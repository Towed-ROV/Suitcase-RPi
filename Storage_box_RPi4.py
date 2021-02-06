# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 13:49:29 2021

@author: fredborg
"""

from dataclasses import dataclass
import json

from NMEA_0183_parser import NMEA_parser
from Project_parser import parser

@dataclass
class Storage_Box():
        def __init__(self):
            self.__json_data = {}
        def update(self,data):
            """
            

            Parameters
            ----------
            data : TYPE
                DESCRIPTION.

            Returns
            -------
            None.

            """
            for keys in data:
                self.__json_data[keys] = data[keys]
                
                
            
                        
                    
                    
                        
                
        def get_sensor(self,category):
            """
            

            Parameters
            ----------
            category : TYPE
                DESCRIPTION.

            Returns
            -------
            TYPE
                DESCRIPTION.

            """
            return self.__json_data[category]
        
        def get_sensor_old(self,category, t = None):
            """
            

            Parameters
            ----------
            category : TYPE
                DESCRIPTION.
            t : TYPE, optional
                DESCRIPTION. The default is None.

            Returns
            -------
            TYPE
                DESCRIPTION.

            """
            d = self.get_sensor(category)
            return "%s:%s"%(category,d)
        
        def get_in_old_style(self):
            """
            

            Returns
            -------
            ret_lst : TYPE
                DESCRIPTION.

            """
            ret_lst = []
            for k in self.keys():
                ret_lst.append(self.get_sensor_old(k))
            return ret_lst
                    
        def get(self):
            """
            

            Returns
            -------
            TYPE
                DESCRIPTION.

            """
            ret_dict = {}
            ret_dict["payload_name"] = "sensor_data"
            l = []
            for k,v in self.__json_data.items():
                l.append({"name": k,"value":v})
            ret_dict["payload_data"]= l
            return ret_dict
        def get_str(self):
            """
            

            Returns
            -------
            TYPE
                DESCRIPTION.

            """
            return json.dumps(self.get())
        def __get_sentence(self):
            [[{"name":k,"value":v} for k,v in self.__json_data.iteritems]]
            return {"payload_type":"sensor_data","payload_data":self.__json_data}
        def keys(self):
            return self.__json_data.keys()
    
#____________________NMEA PARSER
p = parser() 
a = NMEA_parser(p)
b = Storage_Box()

msg1= a.parse_raw_message("Z/#m$SDDPT,,*57")
rmsg2 = "$YXMTW,3.2,C,30,F,262.2,K*07"
msg0= a.parse_raw_message("/n/\n None^d$YXMTW,25.6,C,40 F, 125.6,K*18")
msg2 = a.parse_raw_message(rmsg2)
print("\nnmea parser parsed/n %s \n as:\n %s\n"%(rmsg2,msg2))

#StorageBOX
b.update(msg0)
print("\nfirst message added to Box: \n",b.get_str())

b.update(msg2)
b.update(msg1)
print(b.get())
print("\nafter one eddit and one adding with Null: \n",b.get_str())

msg1= a.parse_raw_message("Z\n/#m$SDDPT,213,long,1232,lat*16")
print("\nadding value to Null sentence:")
b.update(msg1)
print(b.get_str())

print("\ngetting the old data style: \n",b.get_in_old_style())
[print("\nget spesific old :\n ",b.get_sensor_old(m)) for m in b.keys()]

