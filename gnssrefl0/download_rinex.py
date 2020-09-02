# -*- coding: utf-8 -*-
"""
downloads RINEX files
kristine larson
"""
import argparse
import gnssrefl0.gps as g
import gnssrefl0.rnx2snr as rnx

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("station", help="station name", type=str)
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("month", help="month (or day of year)", type=int)
    parser.add_argument("day", help="day (zero if you use day of year earlier)", type=int)
# optional arguments
    parser.add_argument("-rate", default=None, metavar='low',type=str, help="sample rate: low or high")
    parser.add_argument("-archive", default=None, metavar='all',help="archive (unavco,sopac,cddis,sonel,nz,ga,ngs)", type=str)

    args = parser.parse_args()
    year = args.year
    month = args.month
    day = args.day

    if (day == 0):
        # then you are using day of year as input
        year,month,day=g.ydoy2ymd(year, month) 
        doy,cdoy,cyyyy,cyy = g.ymd2doy(year, month, day)
    else:
        doy,cdoy,cyyyy,cyy = g.ymd2doy(year, month, day )
            if args.rate == None:
        rate = 'low'
    else:
        rate = 'high'

    if args.doy_end == None:
        doy2 = doy1
    else:
        doy2 = args.doy_end

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
            archive = 'all'

    g.go_get_rinex_flex(station,year,month,day,rate,archive)
if __name__ == "__main__":
    main()
