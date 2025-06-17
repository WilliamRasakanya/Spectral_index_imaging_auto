#!/usr/bin/env python
# coding: utf-8
__author__ = "William Rasakanya"
__copyright__ = "Copyright 2025"
__credits__ = ["William Rasakanya"]
__license__ = "GPL"
__email__ = "williamrasakanya.astro@gmail.com"

import os, sys
from os import path
import glob
import astropy
from astropy.io import fits
import brats

cwd = os.getcwd()

DATA = cwd + '/data/'
LOGS = cwd + '/logs/'
TXT = cwd + '/txt_files/'

# Bind the BRATS install location
spi_ = brats.Bind("/usr/bin/brats")

h = open(LOGS + 'brats_logs.txt', 'w')
h.write('Running BRATS. \n')
h.write('BRATS python logs to appear here. \n \n')


# Run multiple files in series with execfile():
spi_create = spi_.execfile("spi_commands.txt")
#print(spi_create)
h.write(f'{spi_}' + '\n') # Returns a dictionary {file : returncode}. Returns 0 on success, else returns an error code.

# Alternatively, to have parallel runs with multiexec():
# files = ["./command1.txt", "./commands2.txt"] # List of command files
# runs_ = spi_.multiexec(files, 2) # Syntax: multiexec(list ["files", "to", "process"], int number_of_cores)
# print(runs_)
# h.write(f'{runs_}') # Returns a dictionary {commandfilename : returncode}. Returns 0 on success, else returns an error code.

h.close()

# Fix the header file of the brats output images
#### This fixes the coordinate space of the BRATS images so that they match the input images' coordinates

brats_im = sorted(glob.glob('images/*'))

# reference fits file
ref_fits_file = glob.glob('*fits')[0]

header = fits.getheader(ref_fits_file)

crval1 = header['CRVAL1']
crval2 = header['CRVAL2']
cdelt1 = header['CDELT1']
cdelt2 = header['CDELT2']

for image in brats_im:
    hdu = fits.open(image)
    header_ = hdu[0].header
    data_ = hdu[0].data

    header_['CRVAL1'] = crval1
    header_['CRVAL2'] = crval2
    header_['CDELT1'] = cdelt1
    header_['CDELT2'] = cdelt2
    header_['CTYPE2'] = 'DEC--SIN' # Fix from BRATS naming CTYPE2 = DEC---SIN

    new_im = fits.PrimaryHDU(data = data_, header = header_)
    new_im.writeto(image, overwrite=True)

    hdu.close()

