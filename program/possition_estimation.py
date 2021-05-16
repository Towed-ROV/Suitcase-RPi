from Storage_Box import Storage_Box
from threading import Thread
from math import sqrt, atan, cos, sin
from sophusUtil import calc_big_circle_dist, earth_radius_at_lat, fast_meter_to_gps
from time import monotonic, sleep


class possition_estimation(Thread):
    def __init__(self, box: Storage_Box, cable_length: float = 100, frequency: float = 2):
        super().__init__()
        self.box = box
        self.cable_length = cable_length
        self.last_lat = 0
        self.last_lon = 0
        self.frequency = frequency
        self.dir= 0

    def run(self):
        while True:
            # try:
            start = monotonic()
            lat = self.box.get_sensor_from_tag("gps", "latitude")
            lon = self.box.get_sensor_from_tag("gps", "longitude")
            depth = self.box.get_sensor_from_tag("depth_rov")
            if lat and lon and depth is not None:
                # print("lat,lon", lat, lon)

                lat = float(lat["latitude"])
                lon = float(lon["longitude"])
                depth = float(depth["depth_rov"])
                if not self.last_lon == lon or self.last_lat ==lat:
                    #print(self.last_lon , lon , self.last_lat ,lat)
                    self.dir = atan((lat - float(self.last_lat)) / (((lon - float(self.last_lon)))))
                    self.last_lat = lat
                    self.last_lon = lon
                self.__estimate_pos(lat, lon, depth, dir)

            sleep(1 / self.frequency - (monotonic() - start))

    def __estimate_pos(self, lat, lon, depth, dir):
        """
        calculates an estimated pos forthe ROV, given the depth of the rov

        """

        x = sqrt(self.cable_length ** 2 - depth ** 2)
        travel = cos(dir) * x, sin(dir) * x
        rov_lat, rov_lon = fast_meter_to_gps(lat1=lat, lon1=lon, meterlat=travel[0], meterlon=travel[1])
        self.box.update({"rov_lat": rov_lat})
        self.box.update({"rov_lon": rov_lon})
