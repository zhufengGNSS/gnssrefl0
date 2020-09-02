# gnssrefl0
This package has a new version of my GNSS-IR reflectometry code
Do not use this until I get a chance to confirm that it installs properly.
The main difference bewteen this version and previous versions is that I am 
attempting to use proper python packaging. I have separated out the main
parts of the code and the command line inputs so that you can use the libraries
yourself or do it all from the command line. This should also - hopefully - make
it easier for the production of Jupyter notebooks. The latter are to be developed
by UNAVCO with NASA funding.

# Overview Comments 

The goal of this python repository is to help you compute (and evaluate) GNSS-based 
reflectometry parameters using geodetic data. This method is often
called GNSS-IR, or GNSS Interferometric Reflectometry. There are three main codes:


Upon installation, there are currently three main scripts:

* **rinex2snr** translates RINEX files into SNR files needed for analysis.

* **gnssir** computes reflector heights (RH) from GNSS data.

* **quickLook** gives you a quick (visual) assessment of a file without dealing
with the details associated with **gnssir**.


# Things you need to do 

You need to define (at least) three environment variables:

* EXE = where various RINEX executables will live.  

* ORBITS = where the GPS/GNSS orbits will be stored 

* REFL_CODE = where the reflection code inputs (SNR files and instructions) and outputs (RH)
will be stored (see below)

# Python
See the requirements.txt file

# Non-python
All executables must be stored in the EXE directory

* Required translator CRX2RNX, http://terras.gsi.go.jp/ja/crx2rnx.html

* Optional Fortran RINEX Translator for GPS, the executable must be called gpsSNR.e, https://github.com/kristinemlarson/gpsonlySNR

* Optional Fortran RINEX translator for multi-GNSS, the executable must be called gnssSNR.e, https://github.com/kristinemlarson/gnssSNR


* Optional datatool, teqc is but highly recommended.  There is a list of static executables at the
bottom of [this page](http://www.unavco.org/software/data-processing/teqc/teqc.html)

* Optional datatool, gfzrnx is required if you plan to use the RINEX 3 option. Executables available from the GFZ,
http://dx.doi.org/10.5880/GFZ.1.1.2016.002


Still working on the rest
