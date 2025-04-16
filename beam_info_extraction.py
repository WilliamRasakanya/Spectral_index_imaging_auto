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
import shutil
from astropy.io import fits

cwd = os.getcwd()

DATA = cwd + '/data/'
try:
    os.mkdir(DATA)
except:
    pass

IMAGES = cwd + '/images/'
try:
    os.mkdir(IMAGES)
except:
    pass

LOGS = cwd + '/logs/'
try:
    os.mkdir(LOGS)
except:
    pass

TXT = cwd + '/txt_files/'
try:
    os.mkdir(TXT)
except:
    pass

def main():

    imagefiles = sorted(glob.glob('**.fits'))

    minor = []
    major = []
    pa = []

    nax1 = []
    nax2 = []

    for image in imagefiles:
        header = fits.getheader(image)

        bmin = header['BMIN'] * 60*60 # Convert from degrees to arcsec
        minor.append(bmin)

        bmaj = header['BMAJ'] *60*60 # Convert from degrees to arcsec
        major.append(bmaj)

        bpa = header['BPA']
        pa.append(bpa)

        naxis1 = header['NAXIS1'] # Get pixel axis 1 length
        nax1.append(naxis1)
        
        naxis2 = header['NAXIS2'] # Get pixel axis 2 length
        nax2.append(naxis2)

    # identify the larger BMAJ for smoothing purposes

    larger_major = max(major)
    major_index = major.index(larger_major)
    larger_minor = minor[major_index]

    # Identify the image file with the aformentioned larger BMAJ
    h = open(LOGS + 'beamext_logs.txt', 'w')
    h.write("# Reference image identification for smoothing purposes. \n \n")
    print("image ", imagefiles[major_index], " will be used as a reference,")
    h.write(f"Image {imagefiles[major_index]} will be used as a reference,")
    print("and all other images will be smoothed to its beam size.")
    h.write("and all other images will be smoothed to its beam size. \n")

    larger_bpa = pa[major_index] # Use the BPA of the chosen image

    h.write("Creating full region map...")
    # Create a region file that covers the whole image
    g = open(TXT + 'full_map.reg', 'w')
    g.write('# Region file format: DS9 version 4.1' + '\n')
    g.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1' + '\n')
    g.write('physical' + '\n')
    g.write(f'box({(nax1[major_index] - 1)/2}, {(nax1[major_index] - 1)/2}, {(nax1[major_index] - 1)}, {(nax1[major_index] - 1)}, 0)' + ' # color=#FFFFFF width=2 text={Full_image}') # The last paramenter in the box, the 0, represents the rotation angle. Change as appropriate.
    g.close()

    h.close()

    # print image filename with larger BMIN and BMAJ to a file
    
    g = open(TXT + 'exclude_im.txt', 'w')
    g.write(imagefiles[major_index])
    g.close()

    # Copy the identified image file to the './data' directory
    shutil.copy2(imagefiles[major_index], DATA + imagefiles[major_index])

    # Convert the larger BMIN and BMAJ values and its BPA into strings and add 'arcsec' or 'deg' where applicable

    larger_major = str(larger_major) + 'arcsec'
    larger_minor = str(larger_minor) + 'arcsec'
    if 'deg' not in str(larger_bpa):
        larger_bpa = str(larger_bpa) + 'deg'
    else:
        larger_bpa = str(larger_bpa)
    
    # Write a file that has BMIN, BMAJ etc info
    
    f = open(TXT + 'beam_info.txt', 'w')
    f.write('# beam info to be used in CASA for smoothing' + '\n')
    f.write(larger_minor + '\n')
    f.write(larger_major + '\n')
    f.write(larger_bpa + '\n')
    f.close()

    # Check if noise region file exists
    noise_reg_file = glob.glob('noise*reg')

    if len(noise_reg_file) == 0:
        os.system('python noise_calc.py')

if __name__ == "__main__":
    
    main()
