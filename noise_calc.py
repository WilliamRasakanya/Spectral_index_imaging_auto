#!/usr/bin/env python
# coding: utf-8
__author__ = "William Rasakanya"
__copyright__ = "Copyright 2025"
__credits__ = ["William Rasakanya"]
__license__ = "GPL"
__email__ = "williamrasakanya.astro@gmail.com"

import os
import numpy as np
from astropy.io import fits
from photutils.background import Background2D, SExtractorBackground
from photutils.segmentation import detect_sources
from photutils.utils import circular_footprint
from astropy.stats import SigmaClip
from astropy.wcs import WCS

cwd = os.getcwd()

TXT = cwd + '/txt_files/'
try:
    os.mkdir(TXT)
except:
    pass

f = open(TXT + 'exclude_im.txt') 
fline = f.readlines()
exclude_im = fline[0]
f.close()

image_file = exclude_im
header = fits.getheader(image_file)
wcs = WCS(header)
wcs = wcs.celestial # extract 2D world coordinates
data = fits.getdata(image_file)

if len(data.shape) == 4:
    data = data[0,0,:,:]
elif len(data.shape) == 3:
    data = data[0,:,:]
else:
    data = data

sigma_thresh = 3.0 # change as needed

def process_image(image_filename, sigma=sigma_thresh, maxiters=10, nsigma=3.0, box_size=(50, 50), filter_size=(3, 3), npixels=5, radius=3):

    hdul = fits.open(image_filename)
    data = hdul[0].data

    if len(data.shape) == 4:
        data = data[0,0,:,:]
    elif len(data.shape) == 3:
        data = data[0,:,:]
    elif len(data.shape) == 2:
        data = data

    # Calculate the 2D background and background RMS using SExtractorBackground
    sigma_clip = SigmaClip(sigma=sigma, maxiters=maxiters)
    bkg_estimator = SExtractorBackground()
    bkg = Background2D(data, box_size, filter_size=filter_size, sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)
    background = bkg.background
    background_rms = bkg.background_rms

    # Create a mask for the sources
    threshold = (nsigma * background_rms)  # Using 3 sigma above the background
    segment_img = detect_sources(data, threshold, npixels=npixels)
    footprint = circular_footprint(radius=radius)
    mask = segment_img.make_source_mask(footprint=footprint)

    hdul.close()

    return mask

mask = process_image(image_file)

# Define rectangular noise boxes in the background
# (We'll just chunk the image and keep boxes where there's no detected source)
ny, nx = data.shape
box_size = 100  # Size of each region in pixels
region_coords_fk5 = []

for y in range(0, ny, box_size):
    for x in range(0, nx, box_size):
        sub_mask = mask[y:y+box_size, x:x+box_size]
        if np.nansum(sub_mask) < 0.05 * box_size**2:
            x_center = x + box_size / 2
            y_center = y + box_size / 2
            # Convert pixel (x, y) to world coordinates (RA, Dec)
            ra, dec = wcs.wcs_pix2world(x_center, y_center, 0)
            region_coords_fk5.append((ra, dec, box_size, box_size))  # in pixels, but RA/Dec center

# Convert to DS9 region format (in sky or pixel coords)
if len(region_coords_fk5) > 0:

    region_file = "noise.reg"

    with open(region_file, "w") as f:
        f.write("# Region file format: DS9 version 4.1\n")
        f.write("global color=cyan dashlist=8 3 width=1 font='helvetica 10' select=1 highlite=1 "
                "dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n")
        f.write("fk5\n")

        ra, dec, width_pix, height_pix = region_coords_fk5[0] # one region file
            
        # Approximate conversion of pixel size to arcsec for box display (depends on pixel scale!)
        # Optional: Use WCS to convert pixel scale more accurately if needed
        pixel_scale_deg = np.abs(wcs.wcs.cdelt[0])  # degrees per pixel
        width_deg = width_pix * pixel_scale_deg
        height_deg = height_pix * pixel_scale_deg
        f.write(f"box({ra},{dec},{width_deg}d,{height_deg}d,0)\n")


else:
    print("No noise region. Create one or modify the noise region automation threshold.")
