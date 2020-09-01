# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
# needed?
#import warnings
#warnings.filterwarnings("ignore")
#import cProfile
import subprocess

import gps as g
import argparse
import scipy.interpolate
import scipy.signal
import read_snr_files as snr
import gnssir_python3

# my internal codes for the refraction correction, which are based on
# codes from TU Vienna
import refraction as refr
import datetime
import json
import gnssir_guts as guts
station = 'calc'
year = 2020
month = 8
day = 25
g.big_Disk_in_DC(station,year,month,25)
g.big_Disk_in_DC(station,year,month,24)
g.big_Disk_in_DC(station,year,month,23)
g.big_Disk_in_DC(station,year,month,22)
sys.exit()
exc = g.teqc_version()
doy,cdoy,cyyyy,cyy = g.ymd2doy(year,month,day)
rinexfile =  '/Users/kristine/Downloads' + station + cdoy + '0.' + cyy + 'o'
foutname = 'testing.txt'

let = 'abcdefghijklmnopq';
a=[exc]
for i in range(0,4):
        idtag = let[i:i+1]
        print(i,idtag)
        f1= station + cdoy + idtag + '.' + cyy + 'o'
        a.append(f1)

print(a)
fout = open(foutname,'w')
subprocess.call(a,stdout=fout)
fout.close()

sys.exit()
# want to merge the hourly files into this filename
searchl = station + cdoy + '*' + cyy + 'o'
f1= station + cdoy + 'a.' + cyy + 'o'
f2= station + cdoy + 'b.' + cyy + 'o'


sys.exit()

xdir = str(os.environ['REFL_CODE'])


# need to update this json
with open(xdir + '/input/ac12.json') as f:
    lsp = json.load(f)
extension = '66'
station = 'ac12'
snr_type = 66

direc = xdir + '/' + str(2020) + '/results/' + station + '/' + extension + '/'
outdir = '/Users/kristine/Downloads/Tsunami-2020/test2/'
k=1
ed = 1
year = 2020
for doy in range(180,198):
    for e in np.arange(4,9, ed):
        e1 = e
        e2 = e + 4
        lsp['e1'] = e1; lsp['e2'] = e2 
        fname = direc + str(doy) + '.txt'
        print(lsp)
        print('EL ANGLES', e1,e2)
        if ( e2 <= 12.1):
            guts.gnssir_guts(station,year,doy, snr_type, extension, lsp)
            outfile = outdir + str(k) + '.txt'
            subprocess.call(['mv', fname, outfile ]) 
            k +=1
