# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 13:49:29 2021

@author: fredborg
"""

from dataclasses import dataclass
import json

@dataclass
class Storage_Box():
        def __init__(self, keys):
            self.__json_data = {}
            for key in keys:
                self.__json_data[key] =None
        def update(self,data):
            self.__json_data[data.get("type")] = data["data"]
        
        def get_sensor(self,category):
            return self.__json_data.get(category)
        
        def get(self):
            return self.__json_data
        def get_str(self):
            return json.dumps(self.__json_data)

        
data = {"sensor":"SD","type": "DBT", "data": {"M":100,"f":100,"CS":32}}
a = Storage_Box({"DBT","DPT","MTW","GPS"})
a.update(data)
print(a.get_sensor('DBT'))
print(a.get_str())
