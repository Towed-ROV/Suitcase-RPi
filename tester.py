# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 15:38:35 2021

@author: sophu
"""
from NMEA_0183_server import server as in_server
from Storage_box_RPi4 import Storage_Box
from serial_writer import Serial_Writer as out_server

echo_server = in_server("/dev/ttyAMA0",4800)

GPS_server = in_server("/dev/ttyAMA2",9600)

out = out_server("/dev/ttyAMA1",9600)

box = Storage_Box("suitcase")
while True:
    box.update(echo_server.get_message())
    box.update(GPS_server.get_message())
    print(box.get())
    out.write_serial_data(box.get_in_old_style())
    