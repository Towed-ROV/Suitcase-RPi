# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 15:38:35 2021

@author: sophu
"""
from NMEA_0183_server import server as in_server
from Storage_box_RPi4 import storage_box
from serial_writer import serialWriter as out_server
echo_server = in_server("/dev/ttyAMA0",4800)
GPS_server = in_server("/dev/ttyAMA2",9600)
out = out_server("/dev/USB1",9600)

sensors = {"DBT","DPT","MTW","GPS"}
box = storage_box(sensors)
while True:
    box.recive_data(echo_server.get_message())
    box.recive_data(GPS_server.get_message())
    message = box.get()
    out.write_serial_data(message)
    