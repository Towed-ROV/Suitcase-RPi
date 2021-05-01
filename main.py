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


def start_thread(server):
    connected = False
    try:
        server.daemon = True
        server.start()
        connected = True
    except serial.serialutil.SerialException as e:
        print(format(e))
        return connected
    except Exception as e:
        print(format(e))
        return connected
    return connected

box = Storage_Box("suitcase")
sender = ethernet_sender('tcp://0.0.0.0:8767', box, 2)
print("started program")
echo_server =  nmea_server("/dev/ttyAMA0", 4800, box, 10)
GPS_server = gps_server("/dev/ttyAMA2", 9600, box, 10)
dist_c =  Distance_Calculator(box,62.5,10)
connected_echo= start_thread(echo_server)
connected_gps = start_thread(GPS_server)
start_thread(sender)
start_thread(dist_c)
print("conected to echo: ", connected_echo)
print("conected to GPS: ", connected_gps)
print("started box software")


i= 0
last_time = time.monotonic()
while True:
        if (time.monotonic() - last_time> 30):
            if not connected_echo or not connected_gps:
                if not connected_echo:
                    try:
                        echo_server = nmea_server("/dev/ttyAMA0", 4800, box, 10)
                        connected_echo = True
                    except serial.serialutil.SerialException as e:
                        print(format(e))
                if not connected_gps:
                    try:
                        GPS_server = nmea_server("/dev/ttyAMA2", 9600, box, 20)
                        connected_gps = True
                    except serial.serialutil.SerialException as e:
                        print(format(e))
            i = 0
            last_time = time.monotonic()
        if sender.is_closed():
            try:
                print("error: socket closed")
                sender.connect()
            except Exception as e:
                print(format(e))