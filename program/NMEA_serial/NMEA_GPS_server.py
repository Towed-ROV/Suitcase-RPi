"""
Created on Wed Jan 27 16:57:03 2021.

@author: Fredborg
class for receiving and handling NMEA messages over serial.
"""
import time
import serial
from threading import Thread
import adafruit_gps
import traceback


class GPSserver(Thread):
    """Receives and parses NMEA 0183 messages from a serial port.

    Then it stores the message in a storage box. the NMEA parser can take a
    string input and return a more meaningful version of the data.

        Defines the serial port and parser and other variables and constants.

        Args:
            port (string): the port that the server should connect to and read.
            baudrate: storage_box: frequency:
    """

    def __init__(self, storage_box, baudrate, port, frequency):
        """initialzie the GPS server with storage box and serial port :param
        storage_box: :param baudrate: :param port: :param frequency:

        Args:
            storage_box:
            baudrate:
            port:
            frequency:
        """
        Thread.__init__(self)
        self.__ser = serial.Serial(port,
                                   baudrate,
                                   timeout=1,
                                   stopbits=1,
                                   bytesize=8)
        self.box = storage_box
        self.freq = frequency
        self.gps = adafruit_gps.GPS(self.__ser, debug=False)
        #print(self.gps)

    def run(self):
        """runs the server, it works on a timer. :return:"""
        self.set_up()
        last_print = time.monotonic()
        while True:
            try:
                current = time.monotonic()
                self.gps.update()
                #dt = self.freq-(current - last_print)
                self.update_box()
                last_print = current
                #if dt>0:
                 #   time.sleep(dt)
            except serial.serialutil.SerialException as e:
                traceback.print_exc()

    def update_box(self):
        if not self.gps.has_fix:
            return
        gps_dict = {"gps": {"latitude": self.gps.latitude, "longitude": self.gps.longitude,
                            "speed": self.gps.speed_knots}}
        self.box.update(gps_dict)

    def set_up(self):
        self.gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')
        self.gps.send_command(b'PMTK220,500')