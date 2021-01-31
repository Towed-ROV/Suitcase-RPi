import json

from NMEA_0183_parser import NMEA_parser

class project_parser():
    def __init__(self):
        self.last_message = ""
        self.c_set = set('0123456789.')
        
    def parse_message(self,payload_data):
        parsed_data = {}
        if type(payload_data) is str:
            payload_data = json.loads(payload_data)
        print(type(payload_data))
        payloads = []
        for keys in payload_data.keys():
            payloads.append(json.dumps({"payload_name":keys, "payload_data":self.__order_data(payload_data[keys])}))
        
        last_message = payloads
        return payloads
    
    def __order_data(self, data):
        infos = []
    
        for i,v in enumerate(data):
            if v and type(v) is not str:
                infos.append({data[i+1]:v})
                    
        return infos
    
    
per = project_parser()
    
a = NMEA_parser()
msg = a.parse_raw_message("/n/n None^d$YXMTW,25.6,C,40,F,123.2,K*36")
print(per.parse_message(msg))

print(per.parse_message(a.parse_raw_message("Z/#m$SDDPT,,*57")))

print(per.parse_message(a.parse_raw_message("2312__1@£€6{{[6[]$YXMTW,25.6,C*13")))

