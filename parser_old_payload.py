# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 11:39:26 2021

@author: sophu
"""
import json
class parser:
    def __init__(self):
       self.last_message = None
       
    def parse(self, payload_data):
        if not payload_data:
            return
        if type(payload_data) is str:
            payload_data = json.loads(payload_data)
        payloads = []
        for keys in payload_data.keys():
            for values in payload_data[keys]:
                k = v = None
                if values is str:
                    k = values
                else: 
                    v = values
                    if k and v:
                        payloads.append("<%s%s:%s>"%(keys,k,v))
                    elif v:
                        payloads.append("<%s:%s>"%(keys,v))
        self.last_message = payloads
        return payloads
    
    def __get_first_non_string(self, data):
        for d in data:
            if type(d) is not str:
                return d
        return data