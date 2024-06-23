#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

imagefiles = glob.glob('*.fits')  # Scan cwd for '.fits' files, import and put them in a list

f = open(TXT + 'exclude_im.txt') # read the text in the saved files
fline = f.readlines()
exclude_im = fline[0]
f.close()

g = open(TXT + 'beam_info.txt') # read the text in the saved files
gline = g.readlines()
larger_minor = gline[1][:-1]
larger_major = gline[2][:-1]
larger_bpa = gline[3][:-1]
g.close()

# import fits to casa image format

def import_im(image):
    importfits(fitsimage = image,
            imagename = CASA_out + image[0:-5] + '.im',
            overwrite=True)

# Image-smoothing

def smooth(image):
    if image[12:] not in exclude_im[0:-5] + '.im':
        # smooth other images except the reference image
        imsmooth(imagename = image,
                major = larger_major,
                minor = larger_minor,
                pa = larger_bpa,
                #targetres=True,
                overwrite=True,
                outfile = CASA_out + 'smoothed_' + image[12:])

# image regridding
REGRID = False # set to True if regridding is needed.

def regrid(smoothedfiles):
       # now regrid the images || regrid others wrt a reference image
        imregrid(imagename = smoothedfiles,
                template = exclude_im[0:-5] + '.im',
                overwrite = True,
                output = CASA_out + smoothedfiles[12:-3] + '_regrid.im')

# image export to fits

def export(image):
    exportfits(imagename = image, 
        fitsimage = DATA + image[12:-3]+'.fits', overwrite=True)


if __name__ == '__main__':
    j = 40

    images = sorted(glob.glob('*.fits'))

    pool = Pool(processes=j)
    pool.map(import_im,images)
    pool.close()
    pool.join()

    casa_im = sorted(glob.glob('casa_output/'+'*.im'))

    pool = Pool(processes=j)
    pool.map(smooth,casa_im)
    pool.close()
    pool.join()

    if REGRID == False:
        smoothed_files = sorted(glob.glob('casa_output/' + 'smoothed*'))

        pool = Pool(processes=j)
        pool.map(export,smoothed_files)
        pool.close()
        pool.join()

    elif REGRID == True:
        smoothed_files = sorted(glob.glob('casa_output/' + 'smoothed*'))

        pool = Pool(processes=j)
        pool.map(regrid,smoothed_files)
        pool.close()
        pool.join()

        regridded = sorted(glob.glob('casa_output/' + '*_regrid.im'))

        pool = Pool(processes=j)
        pool.map(export,regridded)
        pool.close()
        pool.join()









# Cleaning up

os.system('rm -r ' + CASA_out)

