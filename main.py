"""
Main program, creates sensor, storage and communications classes.

Created on Wed Mar 10 21:43:01 2021
@author: sophu
"""

from payload_sender import ethernet_sender
from Storage_box_RPi4 import Storage_Box
from NMEA_0183_server import server as nmea_server
from distance_calculator import Distance_Calculator
box = Storage_Box("siutcase")

# from TESTING_SYSTEM import test
# test(box)

sender = ethernet_sender('tcp://192.168.0.110:8765', box, 10)
echo_server = nmea_server("/dev/ttyAMA0", 4800, box, 10)
GPS_server = nmea_server("/dev/ttyAMA2", 9600, box, 20)
dist_c =  Distance_Calculator(box,62.5,10)
echo_server.daemon = True
echo_server.start()
GPS_server.daemon = True
GPS_server.start()
sender.daemon = True
sender.start(dist_c)
