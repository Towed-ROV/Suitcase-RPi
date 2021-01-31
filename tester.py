# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 15:38:35 2021

@author: sophu
"""
from NMEA_0183_server import server as in_server
from Storage_box_RPi4 import Storage_Box
from serial_writer import Serial_Writer as out_server
import json
echo_server = in_server("/dev/ttyAMA0",4800)
GPS_server = in_server("/dev/ttyAMA2",9600)
out = out_server("/dev/ttyAMA1",9600)

sensors = {"DBT","DPT","MTW","GPS"}
box = Storage_Box(sensors)
while True:
    box.update(echo_server.get_message())
    box.update(GPS_server.get_message())
    
    out.write_serial_data(box.get_str())
    