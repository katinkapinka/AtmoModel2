#! /usr/bin/python
# -*- coding: utf-8 -*-
# version 29022012 - TODO: integrate station number
# version 01032012 - parameters from console - station number not working yet
#                  - maybe integrate this routine as function in "own_profile"
'''
Get sounding data from http://weater.uwyo.edu.
'''

import numpy as np
import os
import sys

print("reading args...")
i=1
for arg in sys.argv:
    print(str(i)+arg)
    i=i+1

try:
    year = sys.argv[1]
except IndexError:
    print("You need to specify a year on the command line")
    year = raw_input("year:")

try:
    month = sys.argv[2]
except IndexError:
    print("You need to specify a month on the command line")
    month = raw_input("month:")

try:
    day = sys.argv[3]
except IndexError:
    print("You need to specify a day on the command line")
    day = raw_input("day:")

try:
    time = sys.argv[1]
except IndexError:
    print("You need to specify an hour on the command line")
    time = raw_input("time:")

try:
    station = sys.argv[1]
except IndexError:
    print("You need to specify a station on the command line")
    station = raw_input("station:")

# year="2012"
# month="02"
# day="29"
# time="12"
# station="10410"

outfile="sounding_"+year+"_"+month+"_"+day+".dat"

# os.system("curl -s 'http://weather.uwyo.edu/cgi-bin/sounding?region=europe&TYPE=TEXT%3ALIST&YEAR="+year+"&MONTH="+month+"&FROM=2400&TO=2400&STNM=10410' > "+outfile)

os.system("curl -s 'http://weather.uwyo.edu/cgi-bin/sounding?region=europe&TYPE=TEXT%3ALIST&YEAR="+year+"&MONTH="+month+"&FROM="+day+""+time+"&TO="+day+""+time+"&STNM=10410' > "+outfile)
