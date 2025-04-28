#!/usr/bin/env python
# coding: utf-8
__author__ = "William Rasakanya"
__copyright__ = "Copyright 2025"
__credits__ = ["William Rasakanya"]
__license__ = "GPL"
__email__ = "williamrasakanya.astro@gmail.com"

import os
import glob
from multiprocessing import Pool

cwd = os.getcwd() # current working directory

TXT = cwd + '/txt_files/'

CASA_out = cwd + '/casa_output/'

try:
    os.mkdir(CASA_out)
except:
    pass

DATA = cwd + '/data/'

imagefiles = sorted(glob.glob('*.fits'))

f = open(TXT + 'exclude_im.txt') 
fline = f.readlines()
exclude_im = fline[0]
f.close()

g = open(TXT + 'beam_info.txt') 
gline = g.readlines()
larger_minor = gline[1][:-1]
larger_major = gline[2][:-1]
larger_bpa = gline[3][:-1]
g.close()

# import fits to casa image format

def import_im(image):
    importfits(fitsimage = image,
            imagename = CASA_out + os.path.basename(image)[0:-5] + '.im',
            overwrite=True)

# image regridding

REGRID = False # set to True for regridding. Leave False if there are regridding issues.

def regrid(image):
    # regrid other images wrt a reference image
    imregrid(imagename = image,
            template = exclude_im[0:-5] + '.im',
            output = CASA_out + os.path.basename(image)[0:-3] + '_regrid.im',
            overwrite=True)

# image smoothing

def smooth(image):
    if os.path.basename(image) not in exclude_im[0:-5] + '.im':
        # smooth other images except the reference image
        imsmooth(imagename = image,
                major = larger_major,
                minor = larger_minor,
                pa = larger_bpa,
                targetres = True,
                overwrite = True,
                outfile = CASA_out + 'smoothed_' + os.path.basename(image))

# image export to fits

def export(image):
    exportfits(imagename = image,
        fitsimage = DATA + os.path.basename(image)[0:-3]+'.fits',
        overwrite = True)

if __name__ == '__main__':
    j = 8

    images = sorted(glob.glob('*fits'))

    pool = Pool(processes=j)
    pool.map(import_im, images)
    pool.close()
    pool.join()

    casa_im = sorted(glob.glob(CASA_out + '*.im'))

    if REGRID == False:

        pool = Pool(processes=j)
        pool.map(smooth, casa_im)
        pool.close()
        pool.join()

        smoothed_img = sorted(glob.glob(CASA_out + 'smoothed_*.im'))

        pool = Pool(processes=j)
        pool.map(export, smoothed_img)
        pool.close()
        pool.join()

    if REGRID == True:

        pool = Pool(processes=j)
        pool.map(regrid, casa_im)
        pool.close()
        pool.join()

        regridded = sorted(glob.glob(CASA_out + '*_regrid.im'))

        pool = Pool(processes=j)
        pool.map(smooth,regridded)
        pool.close()
        pool.join()

        smoothed_img = sorted(glob.glob(CASA_out + 'smoothed_*.im'))

        pool = Pool(processes=j)
        pool.map(export, smoothed_img)
        pool.close()
        pool.join()


# Cleaning up

os.system('rm -r ' + CASA_out)
