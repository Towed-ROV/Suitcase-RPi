"""
Storage box for sensor saving.

Created on Sun Jan 31 13:49:29 2021

@author: fredborg
"""

import threading


class Storage_Box:
    """
    Stores sensor data, can give outstrings for sending at will.

    Can recive sensor data form different threads and save them, cann then send
    the data to a new thread as raw data or a string parsed as the project
    parsing.

    the class is has added tags and thread safety to a normal dictonay class.

    """

    def __init__(self, origin):
        self.__json_data = {}
        self.origin = origin
        self.send_tags = ["depth_under_boat", "latitude", "speed",
                          "north_south", "longitude", "north_south",
                          "temprature_in_C", "depth_under_transuducer"]
        self.discard_tags = []
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
                    print("%s  %s" % ("data is not dict but", type(data)))
                return False
            for keys, values in data.items():
                self.__json_data[keys] = values
            return True

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
            try:
                return self.__json_data[category]
            except Exception as e:
                print(format(e))

    def __get_value(self, value_name, sensor):
        """
        returns the value of a spesific sensor
        :param value_name:
        :param sensor: the sensor you want the value from
        :return:
        """
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
            return ret_lst

    def __get_all(self):
        """
        Return all data saved in the storage box, parsed for sending.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        ret_dict = self.__build_dict()
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
            return self.__get_all()

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
        Get the keys in the storage box.

        The keys consists of all the sensors saved in the system.

        Returns
        -------
        TYPE: List
            a list off all the sensors in the system..

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
                    payload_list.append(self.__add_sensor("%s" % (key), values))
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
                if (any(tag in keys or tag in sensor.keys() for tag in tags)):
                    iter_sensor = sensor.copy()
                    for sub_keys in iter_sensor.keys():
                        if not any(sub_keys in tag or tag in sub_keys
                                   for tag in tags):
                            del sensor[sub_keys]
                    for key, values in sensor.items():
                        payload_list.append(self.__add_sensor("%s" % (key), values))

            elif (not sensor is None):
                if any(tag in keys for tag in tags):
                    payload_list.append(self.__add_sensor(keys, sensor))
        return payload_list

    def __add_sensor(self, name, sensor):
        """
        adds a sensor to a dictonary with the parsing for theis system, a sensor can have multiple key value pairs,
        since this is common in the NMEA protocoll.
        :param name: the name of the sensor
        :param sensor: the valuesd of the sensors-
        :return: a dictonary with sensor values
        """
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
                for key, value in sensor.items():
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
            if (tag in key and subtag in value):
                return key

    def __get_name_by_tag(self, tag):
        for key in self.__json_data.keys():
            if tag in key:
                return key

    def get_sensor_from_tag(self, tag, subtag=None):
        with self.lock:
            if subtag:
                name = self.__get_name_by_tag_and_sub(tag, subtag)
            else:
                name = self.__get_name_by_tag(tag)
            ret = self.__json_data.get(name)
            if isinstance(ret, dict):
                return ret
            elif not ret == None:
                return {name: ret}
