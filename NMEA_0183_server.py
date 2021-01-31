
"""
Created on Wed Jan 27 16:57:03 2021

@author: Fredborg
class for receiving and handling NMEA messages over serial.
"""
from NMEA_0183_parser import NMEA_parser
from io import TextIOWrapper, BufferedRWPair
import time
import serial
import json

class server():
    """
    This class receives and parses NMEA 0183 messages from a serial port. 
    """
    def __init__(self,port,baudrate):
        """
        initalizer, defines the serial port and parser and other variables and
        constants.

        Parameters
        ----------
        port: string
            the port that the server should connect to and read.

        """
        self.FILE = "D:\ROV_BATCHELOR\Code\Arduino\echo_sounder\EchoData_parsed.txt"
        self.__parser = NMEA_parser()
        self.__ser = serial.Serial(port,
                                   baudrate, 
                                   timeout=1, 
                                   stopbits=1, 
                                   bytesize=8)
        self.__sio = TextIOWrapper(BufferedRWPair(self.__ser,
                                                  self.__ser))
        self.START_TIME = ""
        self.com_err = 0
        
        
        
    def __get_current_time_str(self):
        """

        Returns
        -------
        string
            returns a string with the current time in the format ss:mm:tt.

        """
        timer = time.localtime()
        return "%i:%i:%i"%(timer.tm_sec,  timer.tm_min, timer.tm_hour)
    
    def __get_current_date_str(self):
        """

        Returns
        -------
        string
            Returns a string with the current time in the format dd:mm:yyyy.

        """
        timer = time.localtime()
        return "%i:%i:%i"%(timer.tm_mday, timer.tm_mon, timer.tm_year)

    def runserver(self):
        """
        main server loop, this loops until failure. It reads the server port
        and parses data it receives.
        """
        self.set_start_time()
        self.__save_to_file( "\n Server started: %s \n" % ( self.START_TIME), 
                                                            self.FILE)
    
        while True:
            sentence = self.get_message()
            if len(sentence) > 1 :
                self.__save_to_file(sentence, self.FILE)
           
    def get_message(self):
        """
        gets a message from the serial port, parses it and returns the parsed
        message.

        Raises
        ------
        e
            if the server has a problem and cannot connect to the serial port
            after multiple attempts, it fails and raises an Exception.

        Returns
        -------
        serial
            a parsed NMEA message.

        """
        try:
            #get data from USBclass server():
            if self.ready():
                time_now = self.get_current_time_str()
                
                data = self.__sio.readline()
                #tries to parse the message, if an error ocours the method
                #exits and prints the message.
                try:
                    parsed_data = self.__parser.parse_raw_message(data)
                except Exception as e:
                    print(format(e))
                    return
                        
                
                #return parsed data
                return "%s : %s \n"%(time_now,parsed_data)
        except serial.SerialException as e:
            print('communication error: ', format(e))
            time.sleep(0.5)
            self.com_err += 1 
            if self.com_err < 5:
                return self.get_message()
            else: raise e
            
    def __save_to_file(self,sentence,file):
        """
        saves a sentence to a speicifed file

        Parameters
        ----------
        sentence : 
            string
            sentence to save.
        file : 
            string
            the file loctation.


        """
        with open(file,'a')  as f:
                f.write(sentence)
                
    def __set_start_time(self):
        """
        sets the start time of the server.

        """
        self.START_TIME = "%s -:- %s" % (self.get_current_date_str(), 
                                         self.get_current_time_str())
        
    def ready(self):
        """

        Returns
        -------
        boolean
            returns true if the server is ready to parse an NMEA message, false 
            otherwise.

        """
        return self.ser.inWaiting() >10
    
