# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 11:22:13 2021

@author: sophu
"""

from NMEA_0183_parser import NMEA_parser
from Storage_box_RPi4 import Storage_Box
from Project_parser import parser

def test():
    #____________________NMEA PARSER
    p = parser() 
    a = NMEA_parser(p)
    b = Storage_Box()
    
    msg1= a.parse_raw_message("Z/#m$SDDPT,,*57")
    rmsg2 = "$YXMTW,3.2,C,30,F,262.2,K*07"
    msg0= a.parse_raw_message("/n/\n None^d$YXMTW,25.6,C,40 F, 125.6,K*18")
    msg2 = a.parse_raw_message(rmsg2)
    print("\nnmea parser parsed/n %s \n as:\n %s\n"%(rmsg2,msg2))
    
    #StorageBOX
    b.update(msg0)
    print("\nfirst message added to Box: \n",b.get_str())
    
    b.update(msg2)
    b.update(msg1)
    [print("\nget spesific:\n", b.get_sensor(m)) for m in b.keys()]
    print("\nafter one eddit and one adding with Null: \n",b.get_str())
    msg1= a.parse_raw_message("Z\n/#m$SDDPT,213,long,1232,lat*16")
    print("\nadding value to Null sentence:")
    b.update(msg1)
    print(b.get_str())
    
    print("\ngetting the old data style: \n",b.get_in_old_style())
    [print("\nget spesific old :\n ",b.get_sensor_old(m)) for m in b.keys()]
    print("\nget super spesific old: ",b.get_sensor_old
          ("Mean_Temprature_Water_C"))
    
          
test()