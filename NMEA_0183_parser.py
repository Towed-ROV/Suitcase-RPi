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
                              "HDG":"Heding_Deviation_and_Variation",
                              "RSA":"Rudder_sensor_angle",
                              "VHW":"Water_Speed_and_heading",
                              "VTG":"Track_made_good_and_ground_speed",
                              "VWR":"Relative_wind_speed_and_angle",
                              "XDR":"Transducer_values",
                              "GSA":"GPS_and_DOP_and_active_satalites",
                              "ZDA":"Time_and_Date-_UTC,_d_m_y_local_time_zone",
                              "AAM":"Waypoint_Arrival_Alarm"}
        self.__sensor_values={   "MTW":["temp_degree","Unit","checsumm"],
                                      "DPT":["depth_relative_to_transuducer","Offsett","checsumm"],
                                      "DBT":["water_depth_feet","feet","water_depth_meters","meters","water_depth_fatoms","fatoms","checsumm"],
                                      "GGA":["UTC time","1-sigma error in latitude","1-sigma error in longitude","1-sigma error in altitude","ID of most likely failed satellite","Probability of missed detection","Estimate of bias in meters","Standard deviation of bias estimate"],
                                      "GLL":["Latitude","N or S ","Longitude","E or W","UTC of this position","Status A - Data Valid, V - Data Invalid"],
                                      "GSV":["Sentence_number","satellites_in_view","satellite_ID","elevation_degrees","azimuth_degrees_true","SNR_dB_(00-99)"],
                                      "HDM":["Heading Degrees_magnetic","M=magnetic"],
                                      "HDT":["Heading_degrees_True","T=true"],
                                      #"LTW":[],
                                      #"MWD":[],
                                      "MWV":["Wind_Angle","R=Relative,T=True","Wind_Speed","Speed_Units","A=Valid_V=Invalid"],
                                      "RMC":["time","status_V=warning","latitude","north_south","longitude","east_west","speed_knots","track_made_good,_deg_true","date_ddmmyy","magnetic_variation_deg","east_west"],
                                      "HDG":["magnetic_sensor_heading_deg","Magnetic_deviation_deg","magnetic_deviation_direction","magnetic_variation_degreees","magnetic_variation_direction"],
                                      "RSA":["StarBoard_or_single_rudder_sensor(\"-\"=turn_to_port)","Status_A=valid_V=invalid","port_rudder_sensor","Status_A=valid_V=invalid"],
                                      "VHW":["degrees_true","T=true","degrees_mag","M=magnetic","speed_knots","N=knots","speed_kmph","K=Km_per_hour"],
                                      "VTG":["track_degrees_true","T=true","Track_degrees_mag","M=magnetic","speed_knots","N=Knots","speed_Km","K=Km_per_h"],
                                      "VWR":["wind_direction_degrees","relative_wind_dirrection","speed_knots","N=Knots","speed_mps","M=meters_per_sec","speed_kmph","=Km_per_h"],
                                      "XDR":["transducer_type","meshurement_data","Units","name_tansducer"],
                                      "GSA":["selection_mode","mode","ID_of_1st_satelite","ID_of_2nd_satelite","ID_of_3rd_satelite","ID_of_4th_satelite","ID_of_5th_satelite","ID_of_6th_satelite","ID_of_7th_satelite","ID_of_8th_satelite","ID_of_9th_satelite","ID_of_10th_satelite","ID_of_11th_satelite","ID_of_12th_satelite","PDOP_meters","HDOP_meters","VDOP_meters"],
                                      "ZDA":["local_zone_minutes_description","local_zone_description(00_to_+-13h)","year","moth","day","time"],
                                      "AAM":["Status_A=Arrival_circle_entered","Status_A=perpendicular_passed_at_waypoint","Arrival_circle_radius","N=nautical_miles","Waypoint_ID"]
                                      
            }
        
        
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
            
            msg_type = parsed_sentence.sentence_type
            data  = self.__order_data(self.__clean_data(parsed_sentence.data),msg_type)
            data_id = self.__get_data_type(msg_type)
            parsed_json = {data_id:data}
            
            
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
        # not have a "$" or "!" sign it's discarded. if a message does not 
        # have a "*" sign, the checksum is missing and the index function 
        # raises an Exception.
        try:
            start = raw_sentence.find('$')+1
            if not start:
                start =raw_sentence.find('!')+1
                if not start:
                    return
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
        
    def __order_data(self, data,data_id):
       ordered_data = {}
       for i,v in enumerate(data):
           if v:
               if data_id in self.__sensor_values.keys() and i< len(self.__sensor_values[data_id]):
                   ordered_data[self.__sensor_values[data_id][i]] = v
               else: ordered_data["value_%s"%(i)]=v
       print(ordered_data)
       return ordered_data
       
       
       
