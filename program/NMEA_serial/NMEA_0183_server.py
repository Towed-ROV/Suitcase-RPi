"""
Created on Wed Jan 27 16:57:03 2021.

@author: Fredborg
class for receiving and handling NMEA messages over serial.
"""
from NMEA_serial.NMEA_0183_parser import NMEA_parser
import time
import serial
from threading import Thread
from pynmea2 import NMEASentence
import traceback


class server(Thread):
    """Receives and parses NMEA 0183 messages from a serial port.

    Then it stores the message in a storage box.
    """

    def __init__(self, port: str, baudrate: int, storage_box, frequency: float, name: str = None):
        """init.

        Defines the serial port and parser and other variables and constants.

        Args:
            port (str): the port that the server should connect to and read.
            baudrate (int):
            storage_box:
            frequency (float):
        """
        Thread.__init__(self)

        self.__parser = NMEA_parser()
        self.__ser = serial.Serial(port,
                                   baudrate,
                                   timeout=1,
                                   stopbits=1,
                                   bytesize=8)
        self.SERVER_START = ""
        self.com_err = 0
        self.box = storage_box
        self.frequency = frequency
        self.endchar = b"\n"
        self.startchar = b"$"
        self.buffer = b""
        self.last_msg = time.monotonic()
        self.running = True
        if name:
            self.name = name
        else:
            self.name = "default"
        self.reciving = True

    def run(self):
        """Run the Thread, reciving nmea data and parsing it."""
        self.running = True
        last = time.monotonic()
        while self.running:
            try:
                current = time.monotonic()
                dt = current - last
                if dt > 1 / self.frequency:
                    message = self.get_message()
                    delivered = self.box.update(message)
                    last = current
                    print(message)
                    if not delivered:
                        self.reciving = False
                    else:
                        self.last_msg = current
                        self.reciving = True
                else:
                    # print("ImpoSleep", dt, 1 / self.frequency)
                    time.sleep(self.frequency - dt)
            except ValueError as e:
                traceback.print_exc()

    @staticmethod
    def __get_current_time_str():
        """Get the current time as a string.

        Returns:
            string: returns a string with the current time in the format
            ss:mm:tt.
        """
        timer = time.localtime()
        return "%i:%i:%i" % (timer.tm_sec, timer.tm_min, timer.tm_hour)

    @staticmethod
    def __get_current_date_str():
        """Get the current time.

        Returns:
            string: Returns a string with the current time in the format
            dd:mm:yyyy.
        """
        timer = time.localtime()
        return "%i:%i:%i" % (timer.tm_mday, timer.tm_mon, timer.tm_year)

    def get_message(self):
        """Get and parse message from the serial port.

        Returns:
            serial: a parsed NMEA message.

        Raises:
            e: if the server has a problem and cannot connect to the serial port
                after multiple attempts, it fails and raises an Exception.
        """
        try:
            if self.ready():
                msg = self.buffer_read()
                parsed_data = self.__parser.parse_raw_message(msg)
                return parsed_data

        except serial.SerialException as e:
            traceback.print_exc()
            self.retry('communication error: ', e)
        except UnicodeDecodeError as e:
            traceback.print_exc()
            self.retry('decode error: ', e)

    def retry(self, error_type, error):
        """tries to get a message again if the system fails, if it fails more
        than 5 times an error is raised. :param error_type: :param error:
        :return:

        Args:
            error_type:
            error:
        """
        print(error_type, format(error))
        time.sleep(0.1)
        self.com_err += 1
        if self.com_err < 5:
            return self.get_message()
        self.com_err = 0
        raise error

    def buffer_read(self):
        """a buffer reader that reads from a spesified value to another
        spesified value. returns a string when it has read a line of data.
        :return:
        """
        buffer = b""
        reading = True
        while reading:
            data = self.__ser.read(1)
            if str(data) == self.startchar:
                buffer = data
            buffer += data
            if data in self.endchar:
                string = str(buffer)
                return string

    def __set_start_time(self):
        """Set the start time of the server.

        Returns:
            None.:
        """
        self.SERVER_START = "%s -:- %s" % (str(self.get_current_date_str()),
                                           str(self.get_current_time_str()))

    def is_connected(self):
        """
        Returns:
            true if the serial is open.
        """
        return self.serial.open()

    def ready(self):
        """Check if there are bytes waiting.

        Returns:
            boolean: returns true if the server is ready to parse an NMEA
            message, false otherwise.
        """
        try:
            return self.__ser.inWaiting() > 0
        except OSError as osErr:
            traceback.print_exc()
            self.delivered = False
            pass

    def send(self, msg: bytes):
        """sends data over the serial. :param msg: :return:

        Args:
            msg (bytes):
        """
        checksum = NMEASentence.checksum(msg)
        msg += checksum
        # print("sending: ", str(msg))
        self.__ser.write(msg)

    def stop(self):
        """
        stops the thread
        """
        self.running = False

