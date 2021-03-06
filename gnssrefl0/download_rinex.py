# -*- coding: utf-8 -*-
"""
downloads RINEX files
kristine larson
2020sep03 - modified environment variable requirement
"""
import argparse
import gnssrefl0.gps as g
#import gnssrefl0.rnx2snr as rnx

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("station", help="station name", type=str)
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("month", help="month (or day of year)", type=int)
    parser.add_argument("day", help="day (zero if you use day of year earlier)", type=int)
# optional arguments
    parser.add_argument("-rate", default=None, metavar='low',type=str, help="sample rate: low or high")
    parser.add_argument("-archive", default=None, metavar='all',help="archive (unavco,sopac,cddis,sonel,nz,ga,ngs)", type=str)
    parser.add_argument("-version", default=None, metavar=2,type=int, help="rinex version (2 or 3)")

    args = parser.parse_args()

#   make sure environment variables exist.  set to current directory if not
    g.check_environ_variables()

#   assign to normal variables
    station = args.station
    year = args.year
    month = args.month
    day = args.day

    if (day == 0):
        # then you are using day of year as input
        doy = month
        year,month,day=g.ydoy2ymd(year, doy) 
    else:
        doy,cdoy,cyyyy,cyy = g.ymd2doy(year,month,day)

    if args.rate == None:
        rate = 'low'
    else:
        rate = 'high'

    archive_list = ['sopac', 'unavco','sonel','cddis','nz','ga','bkg','jeff','ngs']

    if args.version == None:
        version = 2
    else:
        version = args.version
    
    if args.archive == None:
        archive = 'all'
    else:
        archive = args.archive.lower()
        if archive not in archive_list:
            print('You picked an archive that does not exist')
            print('I am going to check the main ones (unavco,sopac,sonel,cddis)')
            print('For future reference: I allow these archives:')
            print(archive_list)
            archive = 'all'


    NS = len(station)
    # RINEX version 3
    if version == 3:
        if NS == 9:
            srate = 30 # rate supported by CDDIS
            fexist = g.cddis3(station, year, doy,srate)
            if not fexist:
                # try again - unavco has 15 sec I believe
                srate = 15
                fexist = g.unavco3(station, year, doy,srate)
            if fexist:
                print('RINEX DOWNLOAD SUCCESSFUL')
        else:
            print('exiting: station names must have 9 characters')
    else: # RINEX VERSION 2
        if NS == 4:
            g.go_get_rinex_flex(station,year,month,day,rate,archive)
        else:
            print('exiting: station names must have 4 characters, lowercase please')

if __name__ == "__main__":
    main()
