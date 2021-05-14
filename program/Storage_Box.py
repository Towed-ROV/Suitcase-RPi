"""
Storage box for sensor saving.

Created on Sun Jan 31 13:49:29 2021

@author: fredborg
"""

import threading
from sophusUtil import print_frame


class Storage_Box:
    """
    Stores sensor data, can give outstrings for sending at will.

    Can recive sensor data form different threads and save them, cann then send
    the data to a new thread as raw data or a string parsed as the project
    parsing.

    the class is has added tags and thread safety to a normal dictonay class.
    """

    def __init__(self, origin):
        """
        initilaize the system, and sets tags.
        :param origin: the location of the sotrage mox
        """
        self.__json_data = {}
        self.origin = origin
        self.send_tags = ["depth_beneath_boat", "latitude", "speed",
                          "north_south", "longitude", "north_south",
                          "temprature_in_C", "depth_under_transuducer", "echo_error", "temprature","rov_lat","rov_lon"]
        self.discard_tags = []
        self.lock = threading.RLock()

    def update(self, data):
        """
         Update the dictonary with new values while beeing threadsafe.

        :param.
        ----------
        :data : dict
            a value : key pair or a set of value key pairs to add to the system.

        :return: true if sucessful
        """
        with self.lock:
            if type(data) is not dict:
                if not isinstance(data, type(None)):
                    print("%s  %s" % ("data is not dict but", type(data)))
                return False
            for keys, values in data.items():
                self.__json_data[keys] = values
            return True

    def get_sensor(self, key):
        """
        get a sensor with a key
        :param key:
        :return: a value defined by the key given
        """
        with self.lock:
            try:
                return self.__json_data[key]
            except Exception as e:
                print(format(e))

    @staticmethod
    def __get_value(key, dict):
        """
        returns a value from a spesific sensor. the sensor is s dictonary
        :param value_name:
        :param sensor:
        :return:
        """
        return dict[key]

    def get_sensor_old(self, key):
        """
        the old parsing for the system, was used before the new protocol was added.
        :param key: the sensor to get
        :return:
        """
        with self.lock:
            sens = self.get_sensor(key)
            return_list = []
            if isinstance(sens, dict):
                for subkey, value in sens.items():
                    return_list.append("<%s_%s:%s>" % (key, subkey, value))
            else:
                return_list.append("<%s:%s>" % (key, sens))
            return return_list

    def get_in_old_style(self):
        """
        returns the storage in the old parsing
        :return: string with old parisng
        """
        with self.lock:
            ret_lst = ["ekkolodd"]
            for k in self.keys():
                ret_lst.extend(self.get_sensor_old(k))
            return ret_lst

    def __get_all(self):
        """
        gets the entire storage, from the class.
        :return: a dictonary containing the entire storage.
        """
        ret_dict = self.__build_dict()
        return ret_dict

    def get_full(self):
        """
        returns the full storage as a a dictonary. this method is thread safe.
        :return: dict with the data
        """
        with self.lock:
            return self.__get_all()

    def get_reduced(self):
        """
        returns a reduced storage as a dictonary, only the sensors saved in the send tags are returned.
        :return: dict with only the key value pairs that have a mathcing tag.
        """
        with self.lock:
            ret_dict = self.__build_sub_dict(self.send_tags)
            return ret_dict

    def __get_sentence(self):
        """
        returns a string with the json data stored in the storage box.
        :return:
        """
        return {"payload_name": "sensor_data",
                "payload_data": self.__json_data}

    def keys(self):
        """
        returns all the keys in the system
        :return: dict.keys in the system
        """
        return self.__json_data.keys()

    def __build_dict(self):
        """
        return a list of values from the storage box, the list has one of each value that is stored in the box.
        :return:
        """
        payload_list = []
        for keys in self.keys():
            sensor = self.get_sensor(keys)
            if isinstance(sensor, dict):
                for key, values in sensor.items():
                    payload_list.append(self.__add_sensor("%s" % key, values))
            else:
                payload_list.append(self.__add_sensor(keys, sensor))
        return payload_list

    def __build_sub_dict(self, tags):
        """
        returns a list containing all objects form the storage box that has one of the tags provided either in the
        sensor name, or in the name of one of the values of the sensors.
        :param tags: tags to check
        :return:
        """
        payload_list = []
        for keys in self.keys():
            if keys in self.discard_tags:
                continue

            sensor = self.get_sensor(keys)
            if isinstance(sensor, dict):
                if any(tag in keys or tag in sensor.keys() for tag in tags):
                    iter_sensor = sensor.copy()
                    for sub_keys in iter_sensor.keys():
                        if not any(sub_keys in tag or tag in sub_keys
                                   for tag in tags):
                            del sensor[sub_keys]
                    for key, values in sensor.items():
                        payload_list.append(self.__add_sensor("%s" % key, values))

            elif sensor is not None:
                if any(tag in keys for tag in tags):
                    payload_list.append(self.__add_sensor(keys, sensor))
        return payload_list

    @staticmethod
    def __add_sensor(name, sensor):
        """
        adds a sensor to a dictonary with the parsing for theis system, a sensor can have multiple key value pairs,
        since this is common in the NMEA protocoll.
        :param name: the name of the sensor
        :param sensor: the valuesd of the sensors-
        :return: a dictonary with sensor values
        """
        sensor_dict = {"name": name, "value": None}
        if isinstance(sensor, dict):
            if len(sensor) > 1:
                value_dict = {}
                for key, value in sensor.items():
                    value_dict[key] = value
                sensor_dict["value"] = value_dict
            else:
                for key, value in sensor.items():
                    sensor_dict["value"] = value
        else:
            sensor_dict["value"] = sensor
        return sensor_dict

    def clear(self):
        """
        clears the storage.
        """
        self.__json_data.clear()

    def __get_name_by_tag_and_sub(self, tag, subtag):
        """
        gets the name of a sensor wich name containes the tag provided AND where one of the value keys in the sensor
        contains the subtag provided. use full if the system imports from multiple different sensor systems with similar
        names.
        :param tag: a tag for the key you are looking for
        :param subtag: a tag for the
        :return:
        """
        for key, value in self.__json_data.items():
            if tag in key and subtag in value:
                return key

    def __get_name_by_tag(self, tag):
        """
        returns the a key if that key contains a specified tag, for example can return the first depth value it finds if
        "depth" is a tag
        :param tag:str that you want to search for
        :return: str with the key if there is one None oterwise.
        """
        for key in self.__json_data.keys():
            if tag in key:
                return key

    def get_sensor_from_tag(self, tag, subtag=None):
        """
        checks the system for a tag, if the tag is pressent returns the sensor assosiated with that tag, else it returns'
        None. the method takes in both a tag and a subtag, if the subtag is provided it only returns if the sensor
        contains a valuekey that matches the subtag and a key that matches the tag.
        :param tag: the tag to search for.
        :param subtag: the subtag to search for
        :return: a dict with the value if its found else None
        """
        with self.lock:
            if subtag:
                name = self.__get_name_by_tag_and_sub(tag, subtag)
            else:
                name = self.__get_name_by_tag(tag)
            ret = self.__json_data.get(name)
            if isinstance(ret, dict):
                return ret
            elif ret is not None:
                return {name: ret}

    def pop_sensor_from_tag(self, tag, subtag=None):
        """
        checks the system for a tag, if the tag is pressent returns the sensor assosiated with that tag, else it returns'
        None. the method takes in both a tag and a subtag, if the subtag is provided it only returns if the sensor
        contains a valuekey that matches the subtag and a key that matches the tag. when it gets the sensor it removes
        it from the system.
        :param tag: the tag to search for.
        :param subtag: the subtag to search for
        :return: a dict with the value if its found else None
        """
        with self.lock:
            try:
                if subtag:
                    name = self.__get_name_by_tag_and_sub(tag, subtag)
                else:
                    name = self.__get_name_by_tag(tag)
                ret = self.__json_data.pop(name)
                if isinstance(ret, dict):
                    return ret
                elif ret is not None:
                    return {name: ret}
            except KeyError:# as key_e:
                pass
                # print_frame("none existant key: ", key_e)
