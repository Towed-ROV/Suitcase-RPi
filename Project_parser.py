import json
"""
class for parsing the data to the new template that we will be using going 
forward
input is keys for sensor type, and value is sensor data
@author Fredborg
"""
class parser():
    """
    """
    def __init__(self):
        self.last_message = ""
        
    def parse(self,payload_data):
        """
        parses a dictonary containing keys of sensor type and value containing
        sensor data. the data can handle json strings or python dicts
        returns the data in a new structure.
        
        Parameters
        ----------
        payload_data : dict or str
            a dictonary or json string with sensor data.

        Returns
        -------
        payloads : list
            a list with dicts containing the data in the form {"payload_type": "sensor name", 
                                                               "payload_data": [sensor_data]}.
            or None if the payload is empty.
        """
        if not payload_data:
            return
        
        if type(payload_data) is str:
            payload_data = json.loads(payload_data)
        d_lst = []
        for keys in payload_data.keys():
            datas = self.__order_data(payload_data[keys])
            for k in datas.keys():
                d_lst.append({"%s_%s"%(keys,k):datas[k]})
        payload_data = {"payload_data":d_lst}
        return payload_data
    
    def __order_data(self, data):
        ordered_data = {}
        for i,v in enumerate(data):
            if v and type(v) is not str:
                ordered_data[data[i+1]] = v
       
        return ordered_data
    


