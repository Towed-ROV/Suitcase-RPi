"""
Created on Wed Jan 27 16:57:03 2021.

@author: Fredborg
class for receiving and handling NMEA messages over serial.
"""
from NMEA_0183_parser import NMEA_parser
import time
import serial
from NMEA_0183_server import server
from threading import Thread

import adafruit_gps

class GPSserver(Thread):
    """
    Receives and parses NMEA 0183 messages from a serial port.

    Then it stores the message in a storage box.
    """

    def __init__(self, port, baudrate, storage_box, frequency):
        """
        init.

        Defines the serial port and parser and other variables and constants.

        Parameters
        ----------
        port: string
            the port that the server should connect to and read.

        """
        Thread.__init__(self)
        self.__ser = serial.Serial(port,
                                   baudrate,
                                   timeout=1,
                                   stopbits=1,
                                   bytesize=8)
        self.box = storage_box
        self.freq = frequency
        self.gps = adafruit_gps.GPS(self.__ser,debug=False)
        print(self.gps)
    
    def run(self):
        
        self.set_up()
        last_print = time.monotonic()
        
        while True:
            try:
                self.gps.update()
            except serial.serialutil.SerialException as e:
                print(format(e))
                
            current = time.monotonic()
            
            if current - last_print > 1/self.freq:
                if not self.gps.has_fix:
                    last_print = current
                    continue
                
                gps_dict = {"gps":{"latitude":self.gps.latitude, "longitude":self.gps.longitude, "speed":self.gps.speed_knots}}
                self.box.update(gps_dict)
                last_print= current
                
    def set_up(self):
        self.gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
        self.gps.send_command(b'PMTK220,500')
    
 