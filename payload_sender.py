# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:42:29 2021.

@author: sophu
"""
from threading import Thread
import zmq
import time


class ethernet_sender(Thread):
    """
    Ethernet transmitter.

    Sends data to the API from the siutcase.
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
            start = time.process_time()

            message = self.box.get_reduced_string()
            self.publish(message)
            end = time.process_time()
            time.sleep(1/self.frequency - (end-start))

    def publish(self, message):
        """

         Parameters.

        ----------

        message : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.socket.send_json(message)

    def get_message(self, reduce=True):
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
