# -*- coding: utf-8 -*-
"""
code is used to translate rinex files into snr file format used for Lomb Scargle applications
author: kristine larson
date: 20 march 2019
19oct20 changed inputs to put doy_end as an optional input rather than requiring it
20apr15 tried to streamline data pick up, eventually add compression

20jul15 added a lot of archives, including new zealand (nz), geoscience Australia (ga), BKG,
and jeff freymueller
fixed access to CDDIS so they don't shut us out October 1.  I also added a lot of new orbit source
including JAXA, SHAO, GRG, and Wuhan

20aug07 added fortran flag
"""
import argparse
import datetime
import os
import sys
import subprocess

import numpy as np

import gnssrefl0.gps as g
import gnssrefl0.rnx2snr as rnx
 
def main():
#
    parser = argparse.ArgumentParser()
    parser.add_argument("station", help="station name", type=str)
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("doy1", help="start day of year", type=int)
    parser.add_argument("snrEnd", help="snr ending", type=str)
    parser.add_argument("orbType", help="orbit type, nav or sp3 (igs,igr,gbm,jax,sha,wum,grg)", type=str)
# optional arguments
    parser.add_argument("-rate", default=None, metavar='low',type=str, help="sample rate: low or high")
    parser.add_argument("-dec", default=0, type=int, help="decimate (seconds)")
    parser.add_argument("-nolook", default='False', metavar='False', type=str, help="True means only use RINEX files on local machine")
    parser.add_argument("-fortran", default='True', metavar='True',type=str, help="True means use Fortran RINEX translators ")
    parser.add_argument("-archive", default=None, metavar='all',help="archive (unavco,sopac,cddis,sonel,nz,ga,ngs)", type=str)
    parser.add_argument("-doy_end", default=None, help="end day of year", type=int)
    parser.add_argument("-year_end", default=None, help="end year", type=int)

    args = parser.parse_args()
#
# rename the user inputs as variables
#
    station = args.station; NS = len(station)
    if (NS == 4):
        print('Assume RINEX 2.11'); version = 2
        station = station.lower()
    elif (NS == 9):
        print('Assume RINEX 3'); version = 3
        station9ch = station.upper()
        station = station[0:4].lower()
    else:
        print('illegal input - Station must have 4 or 9 characters')
        sys.exit()
    year = args.year
    doy1= args.doy1
    snrt = args.snrEnd # string
    isnr = int(snrt)
    orbtype = args.orbType
# currently allowed orbit types
    orbit_list = ['nav', 'igs','igr','gbm','jax','grg','sha','wum']
    if orbtype not in orbit_list:
        print('You picked an orbit type I do not recognize. Here are the ones I allow')
        print(orbit_list)
        sys.exit()

    if args.fortran == 'True':
        fortran = True
    else:
        fortran = False

# if true ony use local RINEX files, which speeds up analysis of local datasets
    nolook = args.nolook
    if nolook == 'True':
        nol = True
    else:
        nol = False

    if args.rate == None:
        rate = 'low'
    else:
        rate = 'high'

    if args.doy_end == None:
        doy2 = doy1
    else:
        doy2 = args.doy_end


# currently allowed archives 
    archive_list = ['sopac', 'unavco','sonel','cddis','nz','ga','bkg','jeff','ngs']
    if args.archive == None:
        archive = 'all'
    else:
        archive = args.archive.lower()
        if archive not in archive_list:
            print('You picked an archive that does not exist')
            print('I am going to check the main ones (unavco,sopac,sonel,cddis)')
            print('For future reference: I allow these archives:') 
            print(archive_list)

    year1=year
    if args.year_end == None:
        year2 = year 
    else:
        year2 = args.year_end

# decimation rate
    dec_rate = args.dec
#
    ann = g.make_nav_dirs(year)

    doy_list = list(range(doy1, doy2+1))
    year_list = list(range(year1, year2+1))
# loop thru years and days 
    for year in year_list:
        for doy in doy_list:
            cdoy = '{:03d}'.format(doy) ; cyy = '{:02d}'.format(year-2000)
            # first, check to see if the SNR file exists
            snre = g.snr_exist(station,year,doy,snrt)
            if snre:
                print('snr file already exists')
            else:
                r = station + cdoy + '0.' + cyy + 'o'
                print(year, doy, ' will try to find/make from : ', r)
                if nol:
                    print('No Look Option')
                    if os.path.exists(r):
                        print('rinex file exists locally')
                        rnx.conv2snr(year, doy, station, isnr, orbtype,rate,dec_rate,archive,fortran) 
                else:
                    print('will look locally and externally')
                    if version == 3:
                        print('rinex 3 search with orbtype ', orbtype)
                        srate = 30 # rate supported by CDDIS 
                        rinex2exists, rinex3name = g.cddis_rinex3(station9ch, year, doy,srate,orbtype)
                        if not rinex2exists:
                        # try again - unavco has 15 sec I believe
                            srate = 15
                            rinex2exists, rinex3name = g.unavco_rinex3(station9ch, year, doy,srate,orbtype)
                        subprocess.call(['rm', '-f', rinex3name]) # remove rinex3 file
                        if rinex2exists:
                            rnx.conv2snr(year, doy, station, isnr, orbtype,rate,dec_rate,archive,fortran) 
                        else:
                            print('rinex file does not exist for ', year, doy)
                    else:
                        print('rinex 2.11 conversion with ', orbtype)
                        rnx.conv2snr(year, doy, station, isnr, orbtype,rate,dec_rate,archive,fortran) 


if __name__ == "__main__":
    main()
