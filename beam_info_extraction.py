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
    # identify the larger BMIN and BMAJ
    # Identify the image file with the aformentioned larger BMIN and BMAJ, and use its BPA
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

IMAGES = cwd + '/images/'
try:
    os.mkdir(IMAGES)
except:
    pass

# NOISE = cwd + '/noise/'
# try:
#     os.mkdir(NOISE)
# except:
#     pass

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
    
    nax1 = []
    nax2 = []
    #wcs = []


    for image in imagefiles:
        header = fits.getheader(image)
    
        bmin = header['BMIN'] * 60*60  # Convert from degrees to arcsec
        minor.append(bmin)
    
        bmaj = header['BMAJ'] * 60*60  # Convert from degrees to arcsec
        major.append(bmaj)
    
        bpa = header['BPA']
        pa.append(bpa)
        
        naxis1 = header['NAXIS1'] # Get pixel axis 1 length
        nax1.append(naxis1)
        
        naxis2 = header['NAXIS2'] # Get pixel axis 2 length
        nax2.append(naxis2)
        
        #wcs_ = WCS(header) # Extract wcs info 
        #wcs.append(wcs_)
    
    # identify the larger BMIN and BMAJ

    larger_minor = max(minor)
    minor_index = minor.index(larger_minor)

    larger_major = max(major)
    major_index = major.index(larger_major)

    # Identify the image file with the aformentioned larger BMIN and BMAJ
    h = open(LOGS + 'beamext_logs.txt', 'w')
    h.write("# Reference image identification for smoothing purposes. \n \n")
    
    if minor_index == major_index:
        print("image ", imagefiles[minor_index], " will be used as a reference,")
        h.write(f"Image {imagefiles[minor_index]} will be used as a reference,")
        print("and all other images will be smoothed to its beam size.")
        h.write("and all other images will be smoothed to its beam size. \n")
        
        larger_bpa = pa[minor_index] # Use the BPA of the chosen image
        
    else:
        print("Error. The indices do not match. Inspect all files' header info")
        h.write("Error. The indices do not match. Inspect all files' header info.")
    
    h.write('\n \n # Checking if both axes lengths are the same for spectral index map creation. \n \n')
    
    if nax1[minor_index] != nax2[minor_index]:
        h.write("The pixel axes lengths are not the same. \n")
        h.write("Consider cropping the image into a square shape. Otherwise, the biggest square with its centre being that of the image will be used. \n")
        h.write("Creating a square region file that tries to cover most of the image...")
        # Create a square region file that tries to cover the whole image
        size_ = min(nax1[minor_index], nax2[minor_index])
        g = open(TXT + 'full_map.reg', 'w')
        g.write('# Region file format: DS9 version 4.1' + '\n')
        g.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1' + '\n')
        g.write('physical' + '\n')
        g.write(f'box({(size_ - 1)/2}, {(size_ - 1)/2}, {(size_ - 1)}, {(size_ - 1)}, 0)' + ' # color=#FFFFFF width=2 text={Full_image}') # The last paramenter in the box, the 0, represents the rotation angle. Change as appropriate.
        g.close()
        
    else:
        h.write("Pixel axes lengths are the same. \n")
        h.write("Creating full region map...")
        # Create a region file that covers the whole image
        g = open(TXT + 'full_map.reg', 'w')
        g.write('# Region file format: DS9 version 4.1' + '\n')
        g.write('global color=green dashlist=8 3 width=1 font="helvetica 10 normal roman" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1' + '\n')
        g.write('physical' + '\n')
        g.write(f'box({(nax1[minor_index] - 1)/2}, {(nax1[minor_index] - 1)/2}, {(nax1[minor_index] - 1)}, {(nax1[minor_index] - 1)}, 0)' + ' # color=#FFFFFF width=2 text={Full_image}') # The last paramenter in the box, the 0, represents the rotation angle. Change as appropriate.
        g.close()
        
    h.close()    
    
    # print image filename with larger BMIN and BMAJ to a file
    
    g = open(TXT + 'exclude_im.txt', 'w')
    g.write(imagefiles[minor_index])
    g.close()

    # Copy the identified image file to the './data' directory

    shutil.copy2(imagefiles[minor_index], DATA + imagefiles[minor_index])


    # Convert the larger BMIN and BMAJ values and its BPA into strings and add 'arcsec' or 'deg' where applicable

    larger_minor = str(larger_minor) + 'arcsec'
    larger_major = str(larger_major) + 'arcsec'
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
    
    
    
if __name__ == "__main__":
    
    main()

