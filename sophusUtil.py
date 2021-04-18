import inspect
import math
import sys
from math import cos, sin, sqrt, asin
line_d = inspect.currentframe
PI =  math.pi # pi
EARTH_CIRCUMFERENCE_M = 4.0075E4 # earth sicumfrence in meters
a = EARTH_RADIUS_EQUATOR = 6335.439E3 #m
b = EARTH_RADIUS_POLE =   6399.594E3 #m
earth_radius_at_lat = lambda lat: sqrt(((a**2 * cos(lat))**2 + (b**2 * sin(lat))**2) / ((a * cos(lat))**2 + (b * sin(lat))**2))
pytagoras = lambda x,y: (x**2+y**2)**(1/2)
pytagoras_round = lambda x,y,desimal: round(pytagoras(x,y),desimal)
calc_big_circle_dist = lambda lat1,lat2,lon1,lon2, radius: (2*radius*asin(sqrt(sin( (lat2-lat1)/2 )**2 + cos(lat1)*cos(lat2) * sin( (lon2-lon1)/2 )**2)))
print_line = lambda *args: print_frame(line_d().f_back,*args)
deg_to_rad = lambda deg: deg * (PI/180)
rad_to_deg = lambda rad: rad * (180/PI)

def print_frame(f:line_d, *args):
    info = inspect.getframeinfo(f)
    print("\n------------------------------------------------------------")
    if len(args):
        for arg in args:
            print("  |==>  message: ", arg, "\n  |------------------------------------------------------------")
    print("  |printed at line: %s\n  |in fuction: %s \n  |in document:%s" % (info.lineno, info.function, info.filename))
    print("------------------------------------------------------------\n")