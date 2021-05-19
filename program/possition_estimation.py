from Storage_Box import Storage_Box
from threading import Thread
from math import sqrt, atan, cos, sin
from sophusUtil import calc_big_circle_dist, earth_radius_at_lat, fast_meter_to_gps
from time import monotonic, sleep
import traceback

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
            try:
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
                        #d1=(lat - float(self.last_lat))
                        #d2=(lon - float(self.last_lon))
                        self.direct = atan(sin(lat**2+lon**2)/cos(lat**2+lon**2))
                        self.last_lat = lat
                        self.last_lon = lon
                    self.__estimate_pos(lat, lon, depth, self.direct)
                sleep(1 / self.frequency - (monotonic() - start))
            except:
                traceback.print_exc()



    def __estimate_pos(self, lat, lon, depth, direct):
        """
        calculates an estimated pos forthe ROV, given the depth of the rov

        """

        x = sqrt(self.cable_length ** 2 - abs(depth) ** 2)
        travel = cos(direct) * x, sin(direct) * x
        rov_lat, rov_lon = fast_meter_to_gps(lat1=lat, lon1=lon, meterlat=travel[0], meterlon=travel[1])
        #print("lat:",lat,"rov_lat:",rov_lat)
        self.box.update({"rov_lat": rov_lat})
        self.box.update({"rov_lon": rov_lon})