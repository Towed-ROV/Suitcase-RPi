import pynmea2
import json
    
"""
Created on Wed Jan 27 2021

@author: Fredborg
@version:0.1

Takes a string input and parses them with the NMEA0183 protocol.
""" 
class NMEA_parser:
    """
    the NMEA parser can take a string input and return a more meaningful 
    version of the data.
    """
    def __init__(self):
        """
        initializer of the class, sets the amount of errors to 0.
        """
        self.__parser_error_count = 0   
        
        
    def parse_nmea_sentence(self,sentence):
        """
        takes a string as an input, checks the length of the string 
        and returns the parsed message as another string. 

        Parameters
        ----------
        sentence : String.
            An NMEA sentence should start with an  identifier such as: SDDBT
            and the different values are comma-separated, it ends with a 
            checksum.
            
         Raises
         ------
         Exception:
             if the sentence cant be parsed the error message is printed and an 
             exception is raised.

        Returns
        -------
        parsed sentence : String.
            A parsed sentence with the talker id, sentence type and 
            data.

        """
        try:
            parsed_sentence= pynmea2.parse(sentence)
            parsed_json = json.dumps({"sensor:" :parsed_sentence.talker,
                                      "type"    :parsed_sentence.sentence_type,
                                      "data"    :parsed_sentence.data})
            return parsed_json
        
        except pynmea2.ParseError as e:
            print('parser error: ',format(e))
            self.__parser_error_count =  self.__parser_error_count +1
            print('parser error count: ', self.__parser_error_count)
            raise Exception(format(e))
            
    def parse_raw_message(self,raw_sentence):
        """
        NMEA sentences from serial communication often start with some 
        unnecessary or invalid data. this message strips that data, before it 
        parses the sentence.

        Parameters
        ----------
        sentence : string
            This message should contain an NMEA message, but it does not need 
            to start or end with it.
        Returns
        -------
        string
             A parsed sentence with the talker id, sentence type and 
            data.

        """
        # finds where the NMEA sentence starts or stops. if the message does 
        # not have a "$" sign it's assumed to start at 0. if a message does not 
        # have a "*" sign, the checksum is missing and the index function 
        # raises an Exception.
        try:
            start = raw_sentence.find('$')+1
            stop = raw_sentence.index('*')+3
        except:
                raise Exception("error: message has no checksum: ", raw_sentence)
        
        # strips the message down to the NMEA sentence
        sentence = raw_sentence[start:stop]
        
        # parses and returns the sentence
        return self.parse_nmea_sentence(sentence)
    
    
    def get_error_count(self):
        """
        Returns
        -------
        int
            returns the amount of times the parser has failed.

        """
        return self.__parser_error_count
    
a = NMEA_parser()
print(a.parse_raw_message("/n/n None^d$YXMTW,25.6,C*13"))
print(a.parse_raw_message("Z/#m$SDDPT,,*57"))
print(a.parse_raw_message("12312__1@£€6{{[6[]$YXMTW,25.6,C*13"))
        