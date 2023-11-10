#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import glob

cwd = os.getcwd() # current working directory

TXT = cwd + '/txt_files/'

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

for image in imagefiles:    # first import fits to create images in casa format
    importfits(fitsimage = image,
            imagename = image[0:-5] + '.im',
            overwrite=True)

casaimages = glob.glob('*.im')

# Image-smoothing

for image in casaimages:
    if image == exclude_im[0:-5] + '.im':
        continue # smooth other images except the reference image

    imsmooth(imagename = image,
            kernel = 'g',
            major = larger_major,
            minor = larger_minor,
            pa = larger_bpa,
            targetres=True,
            overwrite=True,
            outfile = 'smoothed_' + image)
    
smoothedfiles = glob.glob('smoothed_*')

# image regridding

for i in range(0, len(smoothedfiles)):   # now regrid the images || regrid others wrt a reference image
    imregrid(imagename = smoothedfiles[i],
            template = exclude_im[0:-5] + '.im',
            output = smoothedfiles[i][0:-3] + '_regrid.im')

regridded = glob.glob('*regrid.im')

# export casa im file to fits file
 
for image in regridded:
    exportfits(image, cwd + '/data/' + image[0:-3] + '.fits', overwrite=True)

