#! /usr/bin/python
# -*- coding: utf-8 -*-
# version 30012012 - alternative function create_midfile + changed lineformats

'''
Created on Jan 20, 2012

@author: katinkapinka

Create an own atmospheric profile input in MONORTM (Fortran 90) 
format from atmospheric sounding data (provided by the University of Wyoming,
(http://weather.uwyo.edu))
The sounding data is read in and transfered to the specific format,
then appended at the correct position in a MONORTM input file with other
parameters needed for the radiative transfer calculations in the model.
A standard MONORTM input file commences with the record $ and ends with a %,
all previous and following records are ignored.
'''

import sys
import fortranformat as ff
import csv


def read_soundings():
    ''' Read in lines from atmospheric sounding data and store in lists'''
    
    infile = csv.reader(open(infilename, "r"), delimiter=' ', skipinitialspace=True)
    
    i = 1
    for line in infile:
        var=[]
        var.extend(line)
       # print(var) # to test reading
        altsnd.append(float(var[1]))
        psnd.append(float(var[0]))  # could be int
        tsnd.append(float(var[3]))
        wvsnd.append(float(var[5]))
        i = i + 1
    
    print(altsnd)
    print(wvsnd)
    

# def convert_parameters():           # how do I multipy a number to all items of a list?
  #   zm = altsnd[:] / float(1000)
  #   print(zm)

def create_midfile():
    ''' Aggregate data in correct MonoRTM formatting '''
    
    infile = open(infilename,"r")
    midfile = open("midfile","rw")
    
    import pdb
    pdb.set_trace()
    
    i = 1
    
    print(str(len(altsnd)))

    for i in range (1,len(altsnd)):
            
        if i % 2 is 0:       
            print("----------------")
            line = ff.FortranRecordWriter(secondlineformat)
            line.write([altsnd, psnd, tsnd, jcharp, jchart, dens])
        else:
            print("================")
            line = ff.FortranRecordWriter(firstlineformat)
            line.write([wvsnd, 0, 0, 0, 0, 0, 0])
                # line = ff.FortranRecordWriter(firstlineformat).write([wvsnd, 0, 0, 0, 0, 0, 0])
        
        midfile.write(line)
        i = i + 1    

    midfile.close()

def header():
    ''' Write header to midfile with number of layers and description'''
    # str(len(altsnd))+"own model from sounding"

def append_to_mono():
    ''' Append midfile to monofile'''
    # the sounding data should be appended before the line with  %%%

    
# remember there could/should be a header line with # of layers and Titel, could be appended here as well


# ################################################
# Invoke MAIN module
# ################################################

if __name__ == '__main__':

    print("reading args..")
    i = 1
    for arg in sys.argv: 
        print(str(i) + arg)
        i = i + 1
    
    try:
        # read filename argument
        infilename = sys.argv[1]
    except IndexError:
        #    print("got an index error: " + e)
        print("You need to specify an infile on the command line")    
        infilename = raw_input("filename: ")

        # TODO: catch IOError...
    try:
        # read filename argument
        outfilename = sys.argv[2]
    except IndexError:
        #    print("got an index error: " + e)
        print("You need to specify an outfile on the command line")  # in monortm-style: MONORTM.IN  
        outfilename = raw_input("filename: ")

    try:
        # read filename argument
        monofilename = sys.argv[3]
    except IndexError:
        #    print("got an index error: " + e)
        print("You need to specify a monofile on the command line")    
        monofilename = raw_input("filename: ")


    # try:
    infile = open(infilename, "r")        # sounding.dat
    monofile = open(monofilename, "r")    # e.g. MONORTM.IN_test_model0_raw 
    outfile = open(outfilename, "w")    
    midfile = open("midfile", "w")    
    # except NameError:
    
    # #####################################################
    # define variables:
    # from sounding input:
    altsnd = [] # altitude of sounding [m]
    psnd = []   # pressure of sounding [hPa]
    tsnd = []   # temperature of sounding [celsius]
    wvsnd = []  # water vapor mixing ratio [g/kg]
    # for target format:
    zm = []     # boundary altitude [km] not really needed, actually
    # pm = []     # pressure [hPa]
    # tm = []     # temperature [celsius]
    # wv = []     # water vapor mixing ratio [g/kg]
    jsharp = "A"  # for pressure unit hPa
    jchart = "B"  # for temperature unit celsius
    dens = "C222222" # units for wvsnd (C= mixing ratio) and other densities from model 2
    # #####################################################
   
#   lineFormat = "1X, F10.4, F14.2, 14X, I2, F8.3, F8.3, F7.2, F7.3, F8.3, F7.2"
#   targetFormat = "1X, F10.4, F14.2, 14X, I2, F8.3, F8.3, F7.2, F7.3, F8.3, F7.2"
    firstlineformat = '(F10.3, F10.3, F10.3, 5X, A1, A1, 3X, A7)'
    secondlineformat = '(E10.4, F10.3, F10.6, F10.6, F10.6, F10.6, F10.2)'

    # call functions:
    read_soundings()
    # convert_parameters()
    create_midfile()
    header()
    append_to_mono()

    print("done reading args.    ")
    
    print("all done!")
