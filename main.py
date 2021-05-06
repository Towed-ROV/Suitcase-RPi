"""
Main program, creates sensor, storage and communications classes.

Created on Wed Mar 10 21:43:01 2021
@author: sophu
"""

import time

import serial

from Distance_Calculator import Distance_Calculator
from NMEA_0183_server import server as nmea_server
from NMEA_GPS_server import GPSserver as gps_server
from Storage_box_RPi4 import Storage_Box
from payload_sender import ethernet_sender
from sophusUtil import start_thread, print_frame

print_frame("system starting!", ("connect echo, gps and sender."))

box = Storage_Box("suitcase")
sender = ethernet_sender('tcp://127.0.0.1:8787', box, 2)
echo_server = nmea_server(port="COM2", baudrate=4800, storage_box=box, frequency=10)
GPS_server = gps_server(port="COM31", baudrate=9600, storage_box=box, frequency=10)
distance_calc = Distance_Calculator(box)

started_echo_server = start_thread(echo_server)
started_gps_server = start_thread(GPS_server)
started_sender = start_thread(sender)
started_distance_calculator = start_thread(distance_calc)

print_frame("connected to echo {}".format(echo_server),
            "connected to gps: {}".format(started_gps_server),
            "connected to sender {}".format(started_sender),
            "started dist calculator: {}".format(started_distance_calculator))
last_time = time.monotonic()

while True:
    if (time.monotonic() - last_time > 30):
        if not started_echo_server or not started_gps_server:
            if not started_echo_server:
                start_thread(echo_server)
            if not started_gps_server:
                start_thread(gps_server)
        last_time = time.monotonic()
    sender.connect()
