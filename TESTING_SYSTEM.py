# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 11:22:13 2021

@author: sophu
"""

from NMEA_0183_parser import NMEA_parser
from Storage_box_RPi4 import Storage_Box
from Distance_Calculator import Distance_Calculator
import time
def space():
    print("\n\n\n\n\n")
def test():
    #____________________NMEA PARSER

    a = NMEA_parser()
    b = Storage_Box("suitcase")

    dc = Distance_Calculator(box=b)
    test_lst=[  "$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76",
                "$GPGSA,A,3,10,07,05,02,29,04,08,13,,,,,1.72,1.03,1.38*0A",
                "$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70",
                "$GPGSV,3,2,11,02,39,223,19,13,28,070,17,26,23,252,,04,14,186,14*79",
                "$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76",
                "$GPRMC,092750.000,A,5321.6802,N,00630.3372,W,0.02,31.66,280511,,,A*43",
                "$GPGGA,092751.000,5321.6802,N,00630.3371,W,1,8,1.03,61.7,M,55.3,M,,*75",
                "$GPGSA,A,3,10,07,05,02,29,04,08,13,,,,,1.72,1.03,1.38*0A",
                "$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70",
                "$GPGSV,3,2,11,02,39,223,16,13,28,070,17,26,23,252,,04,14,186,15*77",
                "$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76",
                "$GPRMC,092751.000,A,5321.6802,N,00630.3371,W,0.06,31.66,280511,,,A*45"]
    test_lst2 = ["$GPGGA,092750.000,4321.6802,N,00330.3372,W,1,8,1.03,61.7,M,55.2,M,,*72",
                "$GPGSA,A,3,10,07,05,02,29,04,08,13,,,,,1.72,1.03,1.38*0A",
                "$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70",
                "$GPGSV,3,2,11,02,39,223,19,13,28,070,17,26,23,252,,04,14,186,14*79",
                "$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76",
                "$GPRMC,092750.000,A,4321.6802,N,00230.3372,W,0.02,31.66,280511,,,A*46",
                "$GPGGA,092751.000,4321.6802,N,00130.3371,W,1,8,1.03,61.7,M,55.3,M,,*73",
                "$GPGSA,A,3,10,07,05,02,29,04,08,13,,,,,1.72,1.03,1.38*0A",
                "$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70",
                "$GPGSV,3,2,11,02,39,223,16,13,28,070,17,26,23,252,,04,14,186,15*77",
                "$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76",
                "$GPRMC,092751.000,A,4321.6802,N,00930.3371,W,0.06,31.66,280511,,,A*4B"]
    print(dc.check_dist())
    msg1= a.parse_nmea_sentence("$YXMTW,25.6,C*13")

    print(msg1)
    
    rmsg2 = "$SDDPT,10,*56"
    msg0= a.parse_raw_message("$SDDBT,10,f,10,M,10,F*29")
    b.update(msg0)
    print("---------------- this->",b.get_reduced_string())
    msg0= a.parse_raw_message("$SDDBT,12,f,10,M,10,F*2B")
    b.update(msg0)

    print("---------------- this->",b.get_reduced_string())
    msg0= a.parse_raw_message("$SDDBT,10,f,10,M,13,F*2A")
    b.update(msg0)

    print("---------------- this->",b.get_reduced_string())
    msg0= a.parse_raw_message("$SDDBT,10,f,14,M,10,F*2D")
    b.update(msg0)

    print("---------------- this->",b.get_reduced_string())
    msg0= a.parse_raw_message("$SDDBT,11,f,10,M,10,F*28")
    b.update(msg0)

    print("---------------- this->",b.get_reduced_string())
    msg0= a.parse_raw_message("$SDVLW,10,N,5,NF*28")
    b.update(msg0)

    print("---------------- this->",b.get_full_string())
    msg0= a.parse_raw_message("$SDDBT,10,f,102,M,102,F*29")
    b.update(msg0)

    print("---------------- this->",b.get_reduced_string())
    print("---------------- this->",b.get_reduced_string())
    msg4= a.parse_raw_message("$GPAAM,A,A,0.10,N,WPTNME*32")
    msg2 = a.parse_raw_message(rmsg2)
    print("nmea parser parsed/n %s \n as:\n %s\n"%(rmsg2,msg2))
    
    #StorageBOX
    b.update(msg0)
    print("first message added to Box: \n",b.get_full_string())
    
    b.update(msg4)
    b.update(msg2)
    b.update(msg1)
    print("get test")
    space()
    print("\ngetting the old data style: \n",b.get_in_old_style())
    space()
    [print("\nget spesific old :\n ",b.get_sensor_old(m)) for m in b.keys()]
    space()
    print("adding group")
    for i in range(len(test_lst)):
        test_lst[i] = a.parse_raw_message(test_lst[i])
    for dicts in test_lst:
        b.update(dicts)
    b.update(None)
    b.update({"da":"ta"})
    space()
    print(b.get_full_string())
    space()
    print(b.get_in_old_style())
    space()
    print(b.get_reduced_string())
    #b.clear()
    print(b.get_full_string())
    b.update(msg0)
    b.update(msg1)
    b.update(msg2)
    b.update(msg4)
    print(b.get_reduced_string())
    print("_-----------_")
    print(b.get_sensor_from_tag("GPS","latitude"))
    print(b.pop_sensor_from_tag("depth_of_water"))
    print(b.get_sensor_from_tag("depth_of_water"))
    print(b.get_sensor_from_tag("latitude"))
    print("_-----------_")
    print("_-----------_")
    print("_-----------_")
    time.sleep(1)
    print("ch3ckd:",dc.check_dist())
    print("ch3ckd2:",dc.getmsg(dc.check_dist()))
    for i in range(len(test_lst2)):
        test_lst2[i] = a.parse_raw_message(test_lst2[i])
    for dicts in test_lst2:
        b.update(dicts)
    print("ch3ckd2:",dc.getmsg(dc.check_dist()))

    print("ch3ckd2:",dc.getmsg(dc.check_dist()))
    print(b.get_sensor_from_tag("depth_in_M"))
    b.clear()
    print(b.get_full_string(),"was cleared")
    print("end")
test()