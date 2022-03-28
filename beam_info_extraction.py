#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#******************************** Whole procedure *****************************

# Import the necessary python libraries
# create necessary directories
# Scan cwd for '.fits' files
# Import the fits files
# Using astropy:
    # extract beam info from header info
    # identify the larger BMIN, BMAJ, BPA
    # Identify the image file with the aformentioned larger BMIN, BMAJ, BPA
    # Copy the identified image file to the './data' directory
# Using CASA:
    # smooth all other images using the selected beam sizes
    # use exportfits to export the CASA image output directory to a fits file
# copy the newly created smoothed fits files to the './data' directory
# Using BRATS:
    # create a spectral index map

#******************************************************************************

# Obtaining image resolutions and determining the beam sizes

#*************************************************************

# Import the necessary python libraries

import os, sys
from os import path
import glob
import shutil

from astropy.io import fits
from astropy.convolution import Gaussian2DKernel
from scipy.signal import convolve as scipy_convolve
from astropy.convolution import convolve
from radio_beam import Beam, Beams
import astropy.units as u

#_____________________________________________________________________________

# current working directory
cwd = os.getcwd()

# create essential directories
    # BRATS
DATA = cwd + '/data/'
try:
    os.mkdir(DATA)
except:
    pass

OUTPUT = cwd + '/output/'
try:
    os.mkdir(OUTPUT)
except:
    pass

NOISE = cwd + '/noise/'
try:
    os.mkdir(NOISE)
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

#_____________________________________________________________________________

def main():
    
    imagefiles = glob.glob('*.fits')  # Scan cwd for '.fits' files, import and put them in a list

    minor = []
    major = []
    pa = []


    for image in imagefiles:
        header = fits.getheader(image)
    
        bmin = header['BMIN'] * 60*60  #Convert from degrees to arcsec
        minor.append(bmin)
    
        bmaj = header['BMAJ'] * 60*60  #Convert from degrees to arcsec
        major.append(bmaj)
    
        bpa = header['BPA']
        pa.append(bpa)
    
    # identify the larger BMIN, BMAJ, BPA

    larger_minor = max(minor)
    minor_index = minor.index(larger_minor)

    larger_major = max(major)
    major_index = major.index(larger_major)

    larger_bpa = max(pa)
    bpa_index = pa.index(larger_bpa)

    # Identify the image file with the aformentioned larger BMIN, BMAJ, BPA
    if minor_index == major_index:
        print("image", imagefiles[minor_index], "will be used as a reference,")
        print("and all other images will be smoothed to its beam size")
    else:
        print("Error. The indices do not match. Inspect all files header info")
    
    # print image filename with larger BMIN, BMAJ, BPA to a file
    
    g = open(TXT + 'exclude_im.txt', 'w')
    g.write(imagefiles[minor_index])
    g.close()

    # Copy the identified image file to the './data' directory

    shutil.copy2(imagefiles[minor_index], DATA + imagefiles[minor_index])


    # Convert the larger BMIN, BMAJ, BPA value into a string and add 'arcsec' or 'deg' where applicable

    larger_minor = str(larger_minor) + 'arcsec'
    larger_major = str(larger_major) + 'arcsec'
    larger_bpa = str(larger_bpa) + 'deg'
    
    # Write a file that has BMIN, BMAJ etc info
    
    f = open(TXT + 'beam_info.txt', 'w')
    f.write('# beam info to be used in CASA for smoothing' + '\n')
    f.write(larger_minor + '\n')
    f.write(larger_major + '\n')
    f.write(larger_bpa + '\n')
    f.close()
    
    
if __name__ == "__main__":
    
    main()

