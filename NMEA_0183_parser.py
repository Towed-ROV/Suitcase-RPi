import pynmea2
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
        self.__data_types = { "MTW":"Mean_Temprature_Water",
                              "DPT":"Depth_of_water",
                              "DBT":"Depth_below_Transducer",
                              "GGA":"Global_Positions_System_fix_data",
                              "GLL":"Geographic_possition_-_Langitude/Logitude",
                              "GSV":"Satelites_in_view",
                              "HDM":"Heading,_magnetic",
                              "HDT":"Heading,_True",
                              "LTW":"Distance_traveld_throug_water",
                              "MWD":"Wind_direction_and_speed",
                              "MWV":"Wind_speed_and_angle",
                              "RMC":"Recomended_Minimum_Navigation_Information",
                              "HDG":"Heding_-Deviation_and_Variation",
                              "RSA":"Rudder_sensor_angle",
                              "VHW":"Water_Speed_and_heading",
                              "VTG":"Track_made_good_and_ground_speed",
                              "VWR":"Relative_wind_speed_and_angle",
                              "XDR":"Transducer_values",
                              "GSA":"GPS_and_DOP_and_active_satalites",
                              "ZDA":"Time_and_Date-_UTC,_d_m_y_local_time_zone"}
        
        
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
        
            data  = self.__order_data(self.__clean_data(parsed_sentence.data))
            data_id = self.__get_data_type(parsed_sentence.sentence_type)
            parsed_json = {"%s_%s"%(data_id,k):v for k,v in data.items()}
            
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
    
    def __clean_data(self, data):
        return [None if not v else float(v) if all((c in set('1234567890.')) for c in v) else v for v in data] 
    
    def __get_data_type(self, identifier):
        if identifier in self.__data_types:
            return self.__data_types[identifier]
        else:return "%s: %s \n"%("unknow ID",identifier)
        
    def __order_data(self, data):
       ordered_data = {}
       for i,v in enumerate(data):
           if v and type(v) is not str:
               if type(data[i+1]) is str:
                   ordered_data[data[i+1]] = v
               else:
                    ordered_data["value_%s"%(i)]=v
                    
       return ordered_data
       
       
       
