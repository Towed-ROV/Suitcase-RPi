
from threading import Thread
from Storage_box_RPi4 import Storage_Box
from sophusUtil import PI, pytagoras_round, deg_to_rad, earth_radius_at_lat, calc_big_circle_dist
import time

class Distance_Calculator(Thread):
    def __init__(self,box:Storage_Box,start_lat=62.5,to_travel=10):
        Thread.__init__(self)
        self.box = box
        self.last_lat = start_lat
        self.last_lon = 0
        self.earth_radius = earth_radius_at_lat(start_lat)
        self.to_travel = to_travel
        self.getmsg = lambda b: {"has_traveled_set_distance":b}

    def run(self):
        while True:
            traveld = self.check_dist()
            self.box.update(self.getmsg(traveld))
            time.sleep(1)

    def calculate_dist(self,lat1,lat2,lon1,lon2):
        self.last_lon = lon1
        self.last_lat = lat1
        lat1 = deg_to_rad(lat1)
        lat2 = deg_to_rad(lat2)       
        lon1 = deg_to_rad(lon1)
        lon2 = deg_to_rad(lon2)
        dist = calc_big_circle_dist(lat1, lat2, lon1, lon2, self.earth_radius)
        return  dist

    def moved_since_last(self, n_lat,n_lon):
        return self.calculate_dist(n_lat, self.last_lat, n_lon, self.last_lon)

    def check_dist(self):
        gps_lat = self.box.get_sensor_from_tag("gps","latitude")
        gps_lon = self.box.get_sensor_from_tag("gps","longitude")
        if gps_lat and gps_lon:
            lon = gps_lon["longitude"]
            lat = gps_lat["latitude"]
            dist = self.moved_since_last(lat,lon)
            print(dist)
            if abs(dist) >= self.to_travel:
                return True
           
        return False

    def check_dist_t(self,la,lo):
        lat =la
        lon =lo
        dist = self.moved_since_last(lat,lon)
        if abs(dist) >= self.to_travel:
            return True
        else: 
            return False
    
    def update_earth_radius(self, n_lat=None):
        if not n_lat:
            n_lat = self.last_lat
        self.earth_radius = earth_radius_at_lat(n_lat)
    
if __name__ == "__main__":
    box = Storage_Box("test")
    dc = Distance_Calculator(box, 62.5,10)
    a = dc.moved_since_last(0.00000,0.0001)
    d = dc.check_dist_t(0.0000,0.0002)
    dc.to_travel = 12
    c= dc.check_dist_t(0.0000,0.0003)
    print(d,a,c)