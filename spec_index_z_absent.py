#!/usr/bin/bash
# coding: utf-8

# In[ ]:


import numpy as np
from astropy.io import fits
from astropy.stats import SigmaClip
from photutils.background import Background2D, SExtractorBackground
from photutils.segmentation import detect_sources
from photutils.utils import circular_footprint
import glob
from multiprocessing import Pool
import pandas as pd
import re
import logging
import os

cwd = os.getcwd()

TXT = cwd + '/txt_files/'

RESULTS = cwd + '/results/'

NOISE = cwd + '/noise/'

IMAGES = cwd + '/images/'

try:
    os.system(f'mkdir {RESULTS}')
except:
    pass

try:
    os.system(f'mkdir {NOISE}')
except:
    pass

try:
    os.system(f'mkdir {IMAGES}')
except:
    pass

#https://photutils.readthedocs.io/en/stable/background.html

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


DATA = cwd + '/data/'

f = open(TXT + 'exclude_im.txt') # read the text in the saved files. Image used as a reference for wmoothing and perhaps regridding
fline = f.readlines()
exclude_im = fline[0]
f.close()

#from astropy.stats import sigma_clipped_stats, SigmaClip
#from photutils.segmentation import detect_threshold, detect_sources
#from photutils.utils import circular_footprint

def process_image(image_filename, sigma=3.0, maxiters=10, nsigma=3.0, box_size=(50, 50), filter_size=(3, 3), npixels=5, radius=3):
    try:
        hdul = fits.open(image_filename)
        data = hdul[0].data

        if len(data.shape) == 4:
            data = data[0,0,:,:]
        elif len(data.shape) == 3:
            data = data[0,:,:]
        elif len(data.shape) == 2:
            data = data

        header_ = hdul[0].header

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

        # Subtract the detected sources from the original image
        new_mask = mask.astype(float)
        new_mask[new_mask == 1.0] = np.nan
        noise_image = data - new_mask * data

        #noise_image = np.where(mask, np.nan, data)

        # Calculate statistics
        mean = np.nanmean(noise_image)
        median = np.nanmedian(noise_image)
        std = np.nanstd(noise_image)

        # Save the mask to a new FITS file
        header_mask = hdul[0].header
        header_mask['BUNIT'] = ''
        mask_filename = f'{os.path.basename(image_filename)[:-5]}-residual-mask-thres_{nsigma}sigma.fits'
        hdu_mask = fits.PrimaryHDU(data=mask.astype(float), header=header_mask)
        hdu_mask.writeto(NOISE + mask_filename, overwrite=True)

        noise_filename = f'{os.path.basename(image_filename)[:-5]}-residual-thres_{nsigma}sigma.fits'
        hdu = fits.PrimaryHDU(data=noise_image, header=header_)
        hdu.writeto(NOISE + noise_filename, overwrite=True)

        with open(RESULTS+f'stats-{os.path.basename(image_filename)}.txt', 'w') as f:
            f.write(f'Image statistics of the source-subtracted image {noise_filename} \n \n')
            f.write(f'mean: {mean} \n')
            f.write(f'median: {median} \n')
            f.write(f'std: {std} \n')
        
        # Close the original FITS file
        hdul.close()

        logging.info(f"Processed {image_filename} successfully")

        # Return RMS value
        return std

    except Exception as e:
        logging.error(f"Error processing {image_filename}: {e}")
        return None, None



def main():

    files = glob.glob(DATA + '*.fits')

    images = []
    freq = []
    im_data = []

    #std_dev = []

    for i in files:
        im = fits.open(i)
        images.append(im)

        frequency_ = im[0].header['CRVAL3']
        freq.append(float(frequency_))

        if len(im[0].data.shape) == 4:

            data = im[0].data[0,0,:,:]

        elif len(im[0].data.shape) == 3:

            data = im[0].data[0,:,:]

        elif len(im[0].data.shape) == 2:

            data = im[0].data

        #std_dev = std
        #*****

        im_data.append(data)

    std_dev = process_image(DATA+ exclude_im)

    # Initialize spi_data with np.nan values
    spi_data = np.full_like(im_data[0], np.nan, dtype=np.float64)

    for j in range(0, len(im_data[0][:,0])): # dec
        for k in range(0, len(im_data[0][0,:])): # ra
            try:
                log_s = []
    
                log_v = []
    
                for l in range(0, len(im_data)):
    
                    if im_data[l][j,k] >= 3 * (std_dev): # 3 sigma threshold
                        x = np.log10(im_data[l][j,k])
    
                        log_v.append(np.log10(freq[l]))
    
                        log_s.append(x)
    
    
                if len(log_s) > 1:
    
                    # best fit to the data
                    a, b = np.polyfit(log_v, log_s, 1)
    
                    spi_data[j,k] = a #append the best-fit line gradient to the spi map array
    
                else:
                    spi_data[j,k] = np.nan # if flux is too low and does not meat minimum requirements, record spec index as nan
            
            except IndexError:
                continue
    
    
    spi_header = images[0][0].header
    spi_header['BUNIT'] = ''

    keys_to_remove = [key for key in spi_header.keys() if key.endswith('3') or key.endswith('4')]

    for key in keys_to_remove:
        del spi_header[key]

    try:
        del spi_header['OBSERVER']
    except KeyError:
        pass

    field_name = spi_header['OBJECT']

    spi_image = fits.PrimaryHDU(data=spi_data, header=spi_header)
    spi_image.writeto(f'{IMAGES}{field_name}_manual_spi.fits', overwrite=True)


if __name__ == "__main__":

    main()
