# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 12:03:05 2021

@author: sophu
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 13:49:29 2021

@author: fredborg
"""

from dataclasses import dataclass
import json

@dataclass
class Storage_Box:
        def __init__(self):
            self.__json_data = []
            self.keys = []
        def update(self,data):
            for d in data:
                if d["payload_name"] not in self.keys:
                    self.__json_data.append(d)
                    self.keys.append(d["payload_name"])
        
        def get_sensor(self,category):
            if not category or category not in self.keys:
                return
            
            retLst= []
            for d in self.__json_data:
                if d["payload_name"] in category:
                    retLst.append(d)
            if retLst:
                return retLst
        
        
        def get(self):
            return self.__json_data
        def get_str(self):
            return json.dumps(self.__json_data)

        

