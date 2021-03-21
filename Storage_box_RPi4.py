"""
Storage box for sensor saving.

Created on Sun Jan 31 13:49:29 2021

@author: fredborg
"""
    
import json
import threading
import types

class Storage_Box(dict):
    """
    Stores sensor data, can give outstrings for sending at will.

    Can recive sensor data form different threads and save them, cann then send
    the data to a new thread as raw data or a string parsed as the project
    parsing.

    the class is has added tags and thread safety to a normal dictonay class.

    """

    def __init__(self, origin):
        dict.__init__(self)
        self.__json_data = dict(self)
        self.origin = origin
        self.send_tags = ["time", "depth_in_M", "temprature", "latitude",
                          "north_south", "longitude", "north_south", "speed",
                          "heading", "bias"]
        self.lock = threading.RLock()

    def update(self, data):
        """
        Update the dictonary with new values while beeing threadsafe.

        Parameters.

        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        with self.lock:
            if type(data) is not dict:
                if not isinstance(data, type(None)):
                    raise ValueError("%s  %s" %
                                     ("data is not dict but",
                                      type(data)))
                return
            for keys, values in data.items():
                self.__json_data[keys] = values

    def get_sensor(self, category):
        """
        Parameters.

        ----------
        category : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        with self.lock:
            return self.__json_data[category]

    def __get_value(self, value_name, sensor):
        return sensor[value_name]

    def get_sensor_old(self, category, t=None):
        """

        Parameters.

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
        with self.lock:
            sens = self.get_sensor(category)
            return_list = []
            if isinstance(sens, dict):
                for key, value in sens.items():
                    return_list.append("<%s_%s:%s>" % (category, key, value))
            else:
                return_list.append("<%s:%s>" % (category, sens))
            return return_list

    def get_in_old_style(self):
        """
        Send the data using the previous data structure.

        Returns.
        -------
        ret_lst : TYPE
            DESCRIPTION.
        """
        with self.lock:
            ret_lst = []
            ret_lst.append("ekkolodd")
            for k in self.keys():
                ret_lst.extend(self.get_sensor_old(k))
            return json.dumps(ret_lst)

    def __get_all(self):
        """
        Return all data saved in the storage box, parsed for sending.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        ret_dict = {}
        ret_dict["payload_type"] = "sensor_data"

        ret_dict["payload_data"] = self.__build_dict()
        return ret_dict

    def get_full_string(self):
        """
        Return a string verison of the fill string, parsed forsending.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        with self.lock:
            return json.dumps(self.__get_all())

    def get_reduced_string(self):
        """
        Return a string with all data that contains the relevant tags.

        Returns
        -------
        TYPE: String
            A json string parsed as determined by the project.

        """
        with self.lock:
            ret_dict = {}
            ret_dict["payload_type"] = "sensor_data"
            ret_dict["payload_data"] = self.__build_sub_dict(self.send_tags)
            return json.dumps(ret_dict)

    def __get_sentence(self):
        [[{"name": k, "value": v} for k, v in self.__json_data.iteritems]]
        return {"payload_type": "sensor_data",
                "payload_data": self.__json_data}

    def keys(self):
        """
        Get the keys in the storage box.

        The keys consists of all the sensors saved in the system.

        Returns
        -------
        TYPE: List
            a list off all the sensors in the system..

        """
        return self.__json_data.keys()

    def __build_dict(self):
        payload_list = []
        for keys in self.keys():
            sensor = self.get_sensor(keys)
            payload_list.append(self.__add_sensor(keys, sensor))
        return payload_list

    def __build_sub_dict(self, tags):
        payload_list = []
        for keys in self.keys():
            sensor = self.get_sensor(keys)
            if isinstance(sensor, dict):
                if any(tag in keys.lower() for tag in tags) or any(tag in sensor.keys() for tag in tags):
                    iter_sensor = sensor.copy()
                    for sub_keys in iter_sensor.keys():
                        if not any(sub_keys in tag or tag in sub_keys
                                   for tag in tags):
                            del sensor[sub_keys]
                    payload_list.append(self.__add_sensor(keys, sensor))
            else:
                if any(tag in sensor or sensor in tag for tag in tags):
                    payload_list.append(self.__add_sensor(keys, sensor))
        return payload_list

    def __add_sensor(self, name, sensor):
        print(name,sensor)
        sensor_dict = {}
        sensor_dict["name"] = name
        sensor_dict["value"] = None
        if isinstance(sensor, dict):
            if len(sensor) > 1:
                value_dict = {}
                for key, value in sensor.items():
                    value_dict[key] = value
                sensor_dict["value"] = value_dict
            else:
                for key,value in sensor.items():
                    sensor_dict["value"] = value
        else:
            sensor_dict["value"] = sensor
        return sensor_dict

    def clear(self):
        """
        Clear the data from the storage box.

        Returns
        -------
        None.

        """
        self.__json_data.clear()
