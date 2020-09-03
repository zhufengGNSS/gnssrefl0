# -*- coding: utf-8 -*-


import argparse
import datetime
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.interpolate
import scipy.signal
import subprocess
import sys
import warnings

import gnssrefl0.gnssir_guts as guts
import gnssrefl0.gps as g
# do i need these? i don't think so
#import gnssrefl0.refraction as refr
#from gnssrefl0 import gps as g
#from gnssrefl0.read_snr_files as snr



def main():
# pick up the environment variable for where you are keeping your LSP data
    print('=================================================================================')
    print('===========================RUNNING GNSS IR ======================================')
    print('=================================================================================')
 
#
# user inputs the observation file information
    parser = argparse.ArgumentParser()
    parser.add_argument("station", help="station", type=str)
    parser.add_argument("year", help="year", type=int)
    parser.add_argument("doy", help="doy", type=int)
    parser.add_argument("snrEnd", help="snr file ending", type=int)

# optional inputs
    parser.add_argument("-plt", "--plt", default=None, help="ploting is boolean now. Default is True", type=str)
    parser.add_argument("-fr", "--fr", default=None, type=int, help="try -fr 1 for GPS L1 only, or -fr 101 for Glonass L1")
    parser.add_argument("-ampl", "--ampl", default=None, type=float, help="try -ampl 5-6 for minimum spectral amplitude")
    parser.add_argument("-sat", "--sat", default=None, type=int, help="allow individual satellite")
    parser.add_argument("-doy_end", "--doy_end", default=None, type=int, help="doy end")
    parser.add_argument("-year_end", "--year_end", default=None, type=int, help="year end")
    parser.add_argument("-azim1", "--azim1", default=None, type=int, help="lower limit azimuth")
    parser.add_argument("-azim2", "--azim2", default=None, type=int, help="upper limit azimuth")
    parser.add_argument("-nooverwrite", "--nooverwrite", default=None, type=int, help="use any integer to not overwrite")
    parser.add_argument("-extension", "--extension", default=None, type=str, help="extension for result file, useful for testing strategies")
    parser.add_argument("-compress", "--compress", default=None, type=str, help="xz compress SNR files after use")
    parser.add_argument("-screenstats", "--screenstats", default=None, type=str, help="some stats printed to screen(default is True)")
    parser.add_argument("-delTmax", "--delTmax", default=None, type=int, help="Req satellite arc length (minutes)")
    parser.add_argument("-e1", "--e1", default=None, type=str, help="override min elev angle")
    parser.add_argument("-e2", "--e2", default=None, type=str, help="override max elev angle")

    args = parser.parse_args()

#   make sure environment variables exist.  set to current directory if not
    g.check_environ_variables()

#
# rename the user inputs as variables
#
    station = args.station
    year = args.year
    doy= args.doy
    snr_type = args.snrEnd


# get instructions first - not sure the logic will hold
    instructions = str(os.environ['REFL_CODE']) + '/input/' + station + '.json'

    if os.path.isfile(instructions):
        with open(instructions) as f:
            lsp = json.load(f)
    else:
        print('Instruction file does not exist: ', instructions)
        print('Please make with make_json_input.py and run this code again.')
        sys.exit()

    # now check the overrides
    if (args.plt != None):
        if args.plt == 'True':
            lsp['plt_screen'] = True
        if args.plt == 'False':
            lsp['plt_screen'] = False
    else:
        lsp['plt_screen'] = True

    if lsp['plt_screen']:
        print('LSP plots will come to the screen')


    if (args.delTmax != None):
        lsp['delTmax'] = args.delTmax
        print('Using user defined maximum satellite arc time (minutes) ', lsp['delTmax'])

# though I would think not many people would do this ... 
    if (args.compress != None):
        if args.compress == 'True':
            lsp['wantCompression'] = True
        else:
            lsp['wantCompression'] = False


    if args.screenstats == 'False':
        print('no statistics will come to the screen')
        lsp['screenstats'] = False
    else:
        print('no statistics will come to the screen')
        lsp['screenstats'] = True

# in case you want to analyze multiple days of data
    if args.doy_end == None:
        doy_end = doy
    else:
        doy_end = args.doy_end

# in case you want to analyze multiple years of data
    if args.year_end == None:
        year_end = year
    else:
        year_end = args.year_end


# allow people to have an extension to the output file name so they can run different analysis strategies
# this is undocumented and only for Kristine at the moment
    if args.extension == None:
        extension = ''
    else:
        extension = args.extension


# default will be to overwrite
    if args.nooverwrite == None:
        lsp['overwriteResults'] = True
        print('LSP results will be overwritten')
    else:
        lsp['overwriteResults'] = False
        print('LSP results will not be overwritten')

    if (args.e1 != None):
        print('overriding minimum elevation angle: ',args.e1)
        lsp['e1'] = float(args.e1)
    if (args.e2 != None):
        print('overriding maximum elevation angle: ',args.e2)
        lsp['e2'] = float(args.e2)

# number of azimuth regions 
    naz = int(len(lsp['azval'])/2)
# in case you want to look at a restricted azimuth range from the command line 
    setA = 0
    if args.azim1 == None:
        azim1 = 0
    else:
        setA = 1; azim1 = args.azim1

    if args.azim2 == None:
        azim2 = 360
    else:
        azim2 = args.azim2; setA = setA + 1

    if (setA == 2):
        naz = 1; 
        lsp['azval']  = [azim1,  azim2]

# this is for when you want to run the code with just a single frequency, i.e. input at the console
# rather than using the input restrictions
    if args.fr != None:
        lsp['freqs'] = [args.fr]
        print('overriding frequency choices')
    if args.ampl != None:
        print('overriding amplitude choices')
        lsp['reqAmp'] = [args.ampl]

    if args.sat != None:
        print('overriding - only looking at a single satellite')
        lsp['onesat'] = [args.sat]


    print(lsp)

    year_list = list(range(year, year_end+1))
    doy_list = list(range(doy, doy_end+1))
    for year in year_list:
        for doy in doy_list:
            guts.gnssir_guts(station,year,doy, snr_type, extension,lsp)


if __name__ == "__main__":
    main()

