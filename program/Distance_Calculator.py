from threading import Thread
from Storage_Box import Storage_Box
from sophusUtil import deg_to_rad, earth_radius_at_lat, calc_big_circle_dist
import time


class Distance_Calculator(Thread):
    """class that gets the gps cordinates from the system and calculates the
    distance is has traveld using the haversine formulat.
    """

    def __init__(self, box: Storage_Box, start_lat: float = 62.5, to_travel: float = 10):
        """initalizer starts the system and calculates the radius of the earth
        at the provided location :param box: StorageBox :param start_lat: float
        the latitude that is provided :param to_travel: float the meters the
        system needs to travel to report it

        Args:
            box (Storage_Box):
            start_lat (float):
            to_travel (float):
        """
        Thread.__init__(self)
        self.box = box
        self.last_lat = start_lat
        self.last_lon = 0
        self.earth_radius = earth_radius_at_lat(start_lat)
        self.to_travel = to_travel
        self.getmsg = lambda b: {"has_traveled_set_distance": b}

    def run(self):
        while True:
            traveld = self.check_dist()
            self.box.update(self.getmsg(traveld))
            time.sleep(1)

    def calculate_dist(self, lat1, lon1):
        """calculates the distance traveld since the last v :param lat1: :param
        lon1: :return:

        Args:
            lat1:
            lon1:
        """
        lat1 = deg_to_rad(lat1)
        lon1 = deg_to_rad(lon1)
        dist = calc_big_circle_dist(lat1=lat1, lat2=self.last_lat, lon1=lon1, lon2=self.last_lon,
                                    radius=self.earth_radius)
        return dist

    def check_dist(self):
        """checks if the distance traveld since the last point is greater than
        the selected value. :return: true if the new value is reached, false
        otherwise
        """
        gps_lat = self.box.get_sensor_from_tag("gps", "latitude")
        gps_lon = self.box.get_sensor_from_tag("gps", "longitude")
        if gps_lat and gps_lon:
            lon = gps_lon["longitude"]
            lat = gps_lat["latitude"]
            dist = self.calculate_dist(lat, lon)
            if abs(dist) >= self.to_travel:
                self.last_lon = deg_to_rad(lon)
                self.last_lat = deg_to_rad(lat)
                return True
        return False

    def update_earth_radius(self, n_lat):
        """recalculates the radius of the earth. :param n_lat: the latitude for
        the calculation.

        Args:
            n_lat:
        """
        self.earth_radius = earth_radius_at_lat(n_lat)

    def new_earth_radius(self):
        """Calculates the radius at the current location."""
        self.update_earth_radius(self.last_lat)
