# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:42:29 2021.

@author: sophu
"""
import time
from threading import Thread
import traceback
import zmq


class ethernet_sender(Thread):
    """
    Ethernet transmitter.

    Sends data to the API from the suitcase.
    """

    def __init__(self, ip, storage_box, frequncy):
        """
        initilaizes the server, with setting the zmq socket, and adding the storage box
        :param ip:
        :param storage_box:
        :param frequncy:
        """
        Thread.__init__(self)
        self.ip = ip
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(self.ip)
        self.box = storage_box
        self.frequency = frequncy

    def run(self):
        """
        gets and sends data from the storage box, tries to reconect if it'sclosed
        :return:
        """
        while True:
            try:
                if self.is_closed():
                    print("socket is closed", self.is_closed())
                start = time.process_time()
                self.send_sensors()
                self.send_commands()
                dt = start - time.process_time()
                if 1 / self.frequency > dt:
                    time.sleep(1 / self.frequency - dt)

            except ValueError as e:
                traceback.print_exc()
            except TypeError as e:
                traceback.print_exc()

    def send_sensors(self):
        """
        send sensor data over ZMQ
        :return:
        """
        message = self.get_message(reduce=True)
        if message and len(message) > 0:
            self.publish_sensor(message)

    def send_commands(self):
        """
        send commands over ZMQ
        :return:
        """
        message = self.pop_spesific_mesage('has_traveled_set_distance')
        #print(message)
        if len(message) > 0:
            # print(message[0]['value'])
            if message[0]['value']:
                print(message, self.get_spesific_mesage("depth_beneath_boat"))
                # print(message, self.get_spesific_mesage("depth_beneath_boat"))
                # message[0].update({"depth_beneath_boat", self.get_spesific_mesage("depth_beneath_boat")})
                self.publish_command(message)

    def publish_sensor(self, message):
        """
        publishes a zmq message with the "sensor data" payload name.
        :param message: message to be published
        :return: None
        """
        self.send("sensor_data", message)

    def publish_command(self, message):
        """
        publishes a zmq message with the "commands" payload name.
        :param message: message to be published
        :return: None
        """
        self.send("commands", message)

    def send(self, payload_type, message):
        """
        publsihes the a message over zmq
        :param payload_type: the type of the payload.
        :param message: the data ofthe payload
        """
        payload = {"payload_name": payload_type, "payload_data": message}
        # print("sending: \n", payload)
        self.socket.send_json(payload)

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
            return self.box.get_reduced()
        else:
            return self.box.get_full()

    def pop_spesific_mesage(self, tag):
        """
        gets and removes a spesific message from the stroage box. if given a tag.
        :param tag:
        :return:
        """
        sensor = self.box.pop_sensor_from_tag(tag)
        di = []
        if isinstance(sensor, dict):
            for k, v in sensor.items():
                di.append({"name": k, "value": v})
        return di

    def get_spesific_mesage(self, tag):
        """
        gets a spesific message from the stroage box. if given a tag.
        :param tag:
        :return:
        """
        sensor = self.box.get_sensor_from_tag(tag)
        di = []
        if isinstance(sensor, dict):
            for k, v in sensor.items():
                di.append({"name": k, "value": v})
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
        if self.is_closed():
            try:
                print("error: socket closed")
                self.socket.bind(self.ip)
            except Exception as e:
                traceback.print_exc()

    def is_closed(self):
        """
        checks if the socket is closed.
        :return:
        """
        return self.socket.closed
