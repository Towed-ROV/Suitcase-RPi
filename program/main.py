"""
Main program, creates sensor, storage and communications classes.

Created on Wed Mar 10 21:43:01 2021
@author: sophu
"""

import time

from Distance_Calculator import Distance_Calculator
from NMEA_serial.NMEA_0183_server import server as nmea_server
from NMEA_serial.NMEA_GPS_server import GPSserver as gps_server
from Storage_Box import Storage_Box
from ZMQ_in_out.payload_sender import ethernet_sender
from sophusUtil import start_thread, print_frame
from possition_estimation import possition_estimation
from ZMQ_in_out.message_receiver import MessageReceiver

print_frame("system starting!", "connect echo, gps and sender.")
"""
Set up the Threads.
"""
box = Storage_Box("suitcase")

# simulation_time=13/2 #time of one simulation second set to 1 for physical operation
sys_freq =20
sender = ethernet_sender('tcp://127.0.0.1:8790', box, sys_freq)
echo_server = nmea_server(port="COM2", baudrate=4800, storage_box=box, frequency=sys_freq, name="echo_lod")
GPS_server = gps_server(port="COM31", baudrate=9600, storage_box=box, frequency=sys_freq)
position_calc = possition_estimation(box=box, cable_length=200, frequency=sys_freq)
distance_calc = Distance_Calculator(box,freq=sys_freq)
message_reciever = MessageReceiver(box,freq=sys_freq)
"""
start the Theads
"""
running_echo_server = start_thread(echo_server)
running_gps_server = start_thread(GPS_server)
running_sender = start_thread(sender)
started_distance_calculator = start_thread(distance_calc)
running_reciever = start_thread(message_reciever)
running_possition_estimator = start_thread(position_calc)
"""
print Statuses
"""
print_frame("connected to echo {}".format(echo_server),
            "connected to gps: {}".format(running_gps_server),
            "connected to sender {}".format(running_sender),
            "started dist calculator: {}".format(started_distance_calculator))
last_time = time.monotonic()
"""
tries to restart comunication if it failes.
"""
has_error = False
while True:
    dt = time.monotonic() - last_time
    if dt > 15:
        if not running_echo_server or not running_gps_server:
            if not running_echo_server:
                echo_server.stop()
                print("restarting echo")
                start_thread(echo_server)
            if not running_gps_server:
                print("restarting gps")
                gps_server.start()
        elif time.monotonic() - echo_server.last_msg > 5:
            box.update({"echo_error": "echo_lod_has_not_updated in {} sec".format(
                round(time.monotonic() - echo_server.last_msg), 0)})
            has_error = True
        elif has_error:
            box.pop_sensor_from_tag("echo_error")
            has_error = False
        running_echo_server = echo_server.is_alive()
        running_gps_server = GPS_server.is_alive()
        last_time = time.monotonic()
        sender.connect()
        time.sleep(dt)
