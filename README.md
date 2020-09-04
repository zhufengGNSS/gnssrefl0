# gnssrefl0
This package has a new version of my GNSS-IR reflectometry code
Do not use this until I get a chance to confirm that it installs properly.
The main difference bewteen this version and previous versions is that I am
attempting to use proper python packaging. I have separated out the main
parts of the code and the command line inputs so that you can use the libraries
yourself or do it all from the command line. This should also - hopefully - make
it easier for the production of Jupyter notebooks down the road. 

# Overview Comments

The goal of this python repository is to help you compute (and evaluate) GNSS-based
reflectometry parameters using geodetic data. This method is often
called GNSS-IR, or GNSS Interferometric Reflectometry. There are three main codes:


Upon installation, there are currently three main scripts:

* **rinex2snr** translates RINEX files into SNR files needed for analysis.

* **gnssir** computes reflector heights (RH) from GNSS data.

* **quickLook** gives you a quick (visual) assessment of a file without dealing
with the details associated with **gnssir**.


# Environment Variables 

You should define (at least) three environment variables:

* EXE = where various RINEX executables will live.

* ORBITS = where the GPS/GNSS orbits will be stored

* REFL_CODE = where the reflection code inputs (SNR files and instructions) and outputs (RH)
will be stored (see below)

I have set this so that if you do not define these environment variables, it uses the local
directory to store files. For orbits, inputs, and outputs, those are defined starting with the year.

