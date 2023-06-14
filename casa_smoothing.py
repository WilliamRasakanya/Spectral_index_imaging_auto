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

# Remove the identified image file from the list of images to be smoothed

excl_index = imagefiles.index(exclude_im)
del imagefiles[excl_index]

# Image-smoothing

for image in imagefiles:
    imsmooth(imagename = image,
            kernel = 'g',
            major = larger_major,
            minor = larger_minor,
            pa = larger_bpa,
            targetres=True,
            overwrite=True,
            outfile = 'smoothed_' + image + '.im')
    
smoothedfiles = glob.glob('smoothed_*')

# export casa im file to fits file

for image in smoothedfiles:
    exportfits(image, cwd + '/data/' + image + '.fits', overwrite=True)

