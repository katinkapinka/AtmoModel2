#! /usr/bin/python
# -*- coding: utf-8 -*-
# version 31012012 - alternative function create_midfile + changed lineformats + format input changes
# version 16022012 - switched lineformats!! introduced counter 
# version 29022012 - changed iteration in create_midfile - changed fortranformat-routine - now working! 
#                  - changed tsnd.append in read_soundings() - conversion to [km] for altsnd
#                  - first final version
# version 01032012 - renamed outfile for use in MONORTM - cut out the sounding data of infile
#                  - "found" second line of last layer missing (added +1 to counter)
#                  - second final version
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
import os


def read_soundings():
    ''' Read in lines from atmospheric sounding data and store in lists'''
    
    infile = csv.reader(open(infilename, "r"), delimiter=' ', skipinitialspace=True)
    
    i = 0
    for line in infile:

        if i < 10:    # to skip header lines
            i = i + 1      
        elif "</PRE>" in line: # cuts off lines after </PRE>
            break
        elif len(line) > 8:  # cuts off the lines with station data still left at the end
            var=[]
            var.extend(line)
            altsnd.append(float(var[1])/1000)  # conversion to [km]
            psnd.append(float(var[0]))  # could be int
            tsnd.append(float(var[2]))
            wvsnd.append(float(var[5]))

            i = i + 1

    # test sounding lists
   # print(altsnd)
   # print(psnd)
   # print(tsnd)
   # print(wvsnd)
    
    layers = str(len(altsnd))
    print("The number of layers of the sounding is  " + layers)
    return layers

    infile.close()


def create_midfile():
    ''' Aggregate data in correct MonoRTM formatting '''

    midfile = open("midfile","w+b")
   
    # import pdb
    # pdb.set_trace()
    
    i = 1 # for index counting in midfile (double length of variable-lists)
    
    for i in range (1,2*len(altsnd)+1):  # "+1" for "last" second line 

        if i % 2 is 0:       
            wv = wvsnd.pop(0)
            var2 = [wv, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            line = ff.FortranRecordWriter(secondlineformat).write(var2)

            print(line)

        else:
            alt = altsnd.pop(0)
            pres = psnd.pop(0)
            temp = tsnd.pop(0)
            var1 = [alt, pres, temp, jcharp, jchart, dens]

            line = ff.FortranRecordWriter(firstlineformat).write(var1)

            print(line)

        midfile.write(line + '\n')    
        i = i + 1    
    
    midfile.close()


def header():
    ''' Write monofile to outfile and header with number of layers and description'''

    outfile.writelines(monofile)
    header = [read_soundings(), "own model from sounding"]
    line = ff.FortranRecordWriter('(I5, A24)').write(header)
    outfile.write(line + "\n")
    
    monofile.close()


def append_to_out():
    ''' Append midfile to outfile'''
  
    outfile.writelines(midfile)
    outfile.write("-1." + "\n" + "%%%")

    midfile.close()
    outfile.close()

def rename_outfile():
    ''' Rename outfile to suit as input file for MONORTM'''

    newname = "MONORTM.IN_" + infilename[:-4]
    os.rename(outfilename, newname)


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
    midfile = open("midfile", "w+b")    
    # except NameError:
    
    # #####################################################
    # define variables:
    # from sounding input:
    altsnd = [] # altitude of sounding [m]
    psnd = []   # pressure of sounding [hPa]
    tsnd = []   # temperature of sounding [celsius]
    wvsnd = []  # water vapor mixing ratio [g/kg]
    # for target format:
    jcharp = 'A'  # for pressure unit hPa
    jchart = 'B'  # for temperature unit celsius
    dens = 'C222222' # units for wvsnd (C= mixing ratio) and other densities from model 2
    # #####################################################
   
    firstlineformat = '(F10.3, F10.3, F10.3, A6, A1, A10)'
    secondlineformat = '(E10.4, F10.3, F10.6, F10.6, F10.6, F10.6, F10.2)'

    # call functions:
    read_soundings()
    create_midfile()
    header()
    append_to_out()
    rename_outfile()


    print("done reading args.    ")
    
    print("all done!")
