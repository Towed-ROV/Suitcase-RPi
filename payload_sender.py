# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 22:42:29 2021

@author: sophu
"""
from threading import Thread
from Storage_box_RPi4 import Storage_Box
import zmq
import time
class  ethernet_sender(Thread):
    def __init__(self,ip,storage_box,frequncy):
        Thread.__init__(self)
        self.ip = ip
        context = zmq.Context()
        self.socket=context.socket(zmq.PUB)
        self.connect()
        self.box = storage_box
        self.frequency = frequncy
        
    def run(self):
        while True:
            start = time.process_time()
            message = self.box.get_reduced_string()
            self.socket.send_json(message)
          
            end =time.process_time()
            time.sleep(1/self.frequency - (end-start))
    def disconnect(self):
        self.socket.disconnect()

    def connect(self):
        self.socket.bind(self.ip)
        