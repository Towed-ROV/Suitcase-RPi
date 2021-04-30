"""
Main program, creates sensor, storage and communications classes.

Created on Wed Mar 10 21:43:01 2021
@author: sophu
"""

from payload_sender import ethernet_sender
from Storage_box_RPi4 import Storage_Box
from NMEA_0183_server import server as nmea_server
import adafruit_platformdetect.constants.boards as ap_board

from NMEA_GPS_server import GPSserver as gps_server
import serial
import time
import busio
from Distance_Calculator import Distance_Calculator
box = Storage_Box("suitcase")

connected_echo = False
connected_gps = False
sender = ethernet_sender('tcp://0.0.0.0:8767', box, 2)
print("started program")
try:
    echo_server = nmea_server("/dev/ttyAMA0", 4800, box, 10)
    connected_echo = True
    echo_server.daemon = True
    echo_server.start()
    
except serial.serialutil.SerialException as e:
    print(format(e))


except serial.serialutil.SerialException as e:
    print(format(e))
print("conected to echo: ", connected_echo)
try:
    GPS_server = gps_server("/dev/ttyAMA2", 9600, box, 10)
    #connected_gps = True
    #GPS_server.daemon = True
    #GPS_server.start()
    GPS_server.daemon = True
    GPS_server.start()
    
except serial.serialutil.SerialException as e:
    print(format(e))

print("conected to GPS: ", connected_gps)
dist_c =  Distance_Calculator(box,62.5,10)
sender.daemon = True
sender.start()

print("started box software")
dist_c.daemon = True
dist_c.start()
i= 0
last_time = time.process_time()
while True:
        # print(time.process_time() - last_time)
        if (time.process_time() - last_time> 30):
            #print(box.get_full_string(),time.process_time() - last_time)
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
            last_time = time.process_time()
        if sender.is_closed():
            try:
                print("error: socket closed")
                sender.connect()
            except Exeption as e:
                print(format(e))