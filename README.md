# gnssrefl0
This package is a new version of my GNSS-IR reflectometry code. **Do not use this until I get a chance to confirm that it installs properly.**

The main difference bewteen this version and previous versions is that I am
attempting to use proper python packaging rules, LOL. I have separated out the main
parts of the code and the command line inputs so that you can use the gnssrefl0 libraries
yourself or do it all from the command line. This should also - hopefully - make
it easier for the production of Jupyter notebooks. The latter are to be developed
by UNAVCO with NASA funding.


# Overview Comments

The goal of this python repository is to help you compute (and evaluate) GNSS-based
reflectometry parameters using geodetic data. This method is often
called GNSS-IR, or GNSS Interferometric Reflectometry. There are three main codes:


* **rinex2snr** translates RINEX files into SNR files needed for analysis.

* **gnssir** computes reflector heights (RH) from GNSS data.

* **quickLook** gives you a quick (visual) assessment of a file without dealing
with the details associated with **gnssir**.

There is also a RINEX download script **download_rinex**, but it is not required.

# Things You Should Know

You should define three environment variables:

* EXE = where various RINEX executables will live.

* ORBITS = where the GPS/GNSS orbits will be stored. They will be listed under directories by 
year and sp3 or nav depending on the orbit format.

* REFL_CODE = where the reflection code inputs (SNR files and instructions) and outputs (RH)
will be stored (see below). Both SNR files and results will be saved here in year subdirectories.

However, if you do not do this, the code will assume your local working directory (where you installed
the code) is where you want everything to be.

# Python

If you are using the version from gitHub:

* make a directory, cd into that directory, set up a virtual environment, a la python3 -m venv env, activate it

* git clone https://github.com/kristinemlarson/gnssrefl0 

* pip install .

If you use the PyPi version, I think it installs everything for you??? (right now it is on test.pypi.org)

# Non-python in the code

All executables should be stored in the EXE directory.  If you do not define EXE, it will look for them in your 
local working directory.  The Fortran translators are much faster than using python. But if you don't want to use them,
they are optional, that's fine. FYI, the python version is slow not because of the RINEX - it is because you need to calculate
a crude model for satellite coordinates in this code. And that takes cpu time....

* Required translator for compressed RINEX files. CRX2RNX, http://terras.gsi.go.jp/ja/crx2rnx.html

* Optional Fortran RINEX Translator for GPS, the executable must be called gpsSNR.e, https://github.com/kristinemlarson/gpsonlySNR

* Optional Fortran RINEX translator for multi-GNSS, the executable must be called gnssSNR.e, https://github.com/kristinemlarson/gnssSNR

* Optional datatool, teqc, is highly recommended.  There is a list of static executables at the
bottom of [this page](http://www.unavco.org/software/data-processing/teqc/teqc.html)

* Optional datatool, gfzrnx is required if you plan to use the RINEX 3 option. Executables available from the GFZ,
http://dx.doi.org/10.5880/GFZ.1.1.2016.002


# Making SNR files from RINEX files

I run a lowercase shop. Please name RINEX files accordingly and use lowercase station names.

A RINEX file has extraneous information in it (the data used for positioning) - and does not provide some of the 
information needed (elevation and azimuth angles) for reflectometry. The first task you 
have is to translate a data file from
RINEX into what I will call a SNR format - and to calculate those geometric angles.  
For the latter you will need an orbit file. If you tell it which
kind of orbit file you want, the code will go get it for you.  
Secondly, you will need to decide how much of the data file you want to save. If you are new
to the systems, I would choose **option 99**, which is all data between elevation angles of 5 and 30 degrees.

The command line driver is **rinex2snr**. You need to tell the porgram the name of the station,
the year and doy of year, your orbit file preference, and your SNR format type.
A sample call for a station called p041, restricted to GPS 
satellites, on day of year 132 and year 2020 would be:


*rinex2snr p041 2020 132 99 nav*

If the RINEX file for p041 is in your local directory, it will translate it.  If not, 
it will check four archives (unavco, sopac, cddis, and sonel) to find it. 
I will also search ga (geoscience Australia), nz (New Zealand), ngs, and bkg if you invoke -archive,
e.g.

*rinex2snr tgho 2020 132 99 nav -archive nz*
 

If your station name has 9 characters, the code assumes you are looking for a
RINEX 3 file. However, it will store the SNR data using the normal
4 character name.


The snr options are always two digit numbers.  Choices are:

- 99 is elevation angles of 5-30 degrees  (most applications)

- 88 is elevation angles of 5-90 degrees

- 66 is elevation angles less than 30 degrees

- 50 is elevation angles less than 10 degrees (tall, high-rate applications)

orbit file options:

- nav : GPS broadcast, perfectly adequate for reflectometry
- igs : IGS precise, GPS only
- igr : IGS rapid, GPS only
- jax : JAXA, GPS + great for getting Glonass within a few days
- gbm : GFZ Potsdam, multi-GNSS, not rapid
- grg: French group, GPS, Galileo and Glonass, not rapid
- sha : Shanghao, multi-GNSS, not rapid
- wum : Wuhan, multi-GNSS, not rapid

