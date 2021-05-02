# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:42:29 2021.

@author: sophu
"""
from threading import Thread
import zmq
import time
import json

class ethernet_sender(Thread):
    """
    Ethernet transmitter.

    Sends data to the API from the suitcase.
    """

    def __init__(self, ip, storage_box, frequncy):
        """
         Parameters.

        ----------

        ip : TYPE

            DESCRIPTION.
        storage_box : TYPE
            DESCRIPTION.

        frequncy : TYPE

            DESCRIPTION.

        Returns
        -------
        None.

        """
        Thread.__init__(self)
        self.ip = ip
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.connect()
        self.box = storage_box
        self.frequency = frequncy

    def run(self):
        """


        Return.

        -------

        None.

        """
        while True:
            try:
                start = time.process_time()
                message = self.get_message(reduce=True)
                if message and len(message) >0:
                    self.publish_sensor(message)
                message = self.get_spesific_mesage("has_traveled_set_distance")
                if len(message) and message[0]['value']:
                    self.publish_command(message)
                end = time.process_time()
                time.sleep(1/self.frequency - (end-start))
                if self.is_closed():
                    print("socket is closed",self.is_closed())
                    self.connect()
            except ValueError as e:
                print(format(e))
            
    def publish_sensor(self, message):
        """

         Parameters.

        ----------

        message : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        payload ={}
        payload["payload_name"]= "sensor_data"
        payload["payload_data"]= message
        print("sending:",payload,"\n")
        self.socket.send_json(payload)

    def publish_command(self, message):
        """

         Parameters.

        ----------

        message : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        payload = {}
        payload["payload_name"] = "commands"
        payload["payload_data"] = message
        print("sending: \n", payload, message)
        self.socket.send_string(json.dumps(payload))
        

    def get_message(self, reduce=False):
        """
        Get a message from the storage box.

         Parameters.
        ----------
        reduce : TYPE, optional
            DESCRIPTION. The default is True.
            If it's set to false return a string of all data is sent,
            else only a reduced version of the string is sent.

        Returns
        -------
        TYPE: String
            a json string from the storage box.

        """
        if reduce:
            return self.box.get_reduced_string()
        else:
            return self.box.get_full_string()

    def get_spesific_mesage(self,tag):
        sensor = self.box.get_sensor_from_tag(tag)
        di=[]
        if isinstance(sensor,dict):
            for k,v in sensor.items():
                di.append({"name":k,"value":v})
        return di

    def disconnect(self):
        """
        Disconnect from the socket.

        Returns.
        -------
        None.

        """
        self.socket.disconnect()

    def connect(self):
        """

        Connect the socket to the spesific IP.

        Returns.
        -------
        None.

        """
        self.socket.bind(self.ip)
    
    def is_closed(self):
        return self.socket.closed
