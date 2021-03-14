"""
Storage box for sensor saving.

Created on Sun Jan 31 13:49:29 2021

@author: fredborg
"""

from dataclasses import dataclass
import json
import threading


@dataclass
class Storage_Box:
    """
    Storessensor data, can give outstrings for sending at will.

    Can recive sensor data form different threads and save them, cann then send
    the data to a new thread as raw data or a string parsed as the project
    parsing.

    """

    def __init__(self, origin):
        self.__json_data = {}
        self.origin = origin
        self.send_tags = ["time", "depth", "Temprature", "latitude",
                          "north_south", "longitude", "north_south", "speed",
                          "heading", "bias"]
        self.lock = threading.RLock()

    def update(self, data):
        """
        Parameters.

        ----------
        data : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        with self.lock:
            if not data:
                return
            for keys in data.keys():
                self.__json_data[keys] = data[keys]

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
            d = []
            for keys in sens.keys():
                d.append("<%s_%s:%s>" % (category, keys, sens[keys]))
            return d

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
        d = {}
        d["origin"]: self.origin
        for keys in self.keys():
            sensor = self.get_sensor(keys)
            for value_keys in sensor.keys():
                k = "%s_%s" % (keys, value_keys)
                d[k] = sensor[value_keys]
        return d

    def __build_sub_dict(self, tags):
        d = {}
        d["origin"]: self.origin

        for keys in self.keys():
            sensor = self.get_sensor(keys)
            for value_keys in sensor.keys():

                if(any(tag.lower() in value_keys.lower() for tag in tags)):
                    k = "%s_%s" % (keys, value_keys)
                    d[k] = sensor[value_keys]
        return d