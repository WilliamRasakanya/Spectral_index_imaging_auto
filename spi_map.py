#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# In[ ]:


#****************Whole procedure****************

# Create a file and write commands for BRATS to create spectral index map
# Use BRATS to create said map

#************************************************

# Import libraries

import os, sys
from os import path

cwd = os.getcwd() # current working directory

TXT = cwd + 'txt_files/'

g = open(TXT + 'spi_commands.txt', 'w')
g.write('sigma')
g.write('5')
g.write('export')
g.write('exportasfits')
g.write('imageloc')
g.write('images')
g.write('load')
g.write('data')
g.write('noise/noise.reg') # noise region
g.write('txt_files/full_map.reg') # region file path (Default will use the full map)
g.write('0.0474') # redshift of the source of interest
g.write('specindexcalctype')
g.write('2')
g.write('fluxcalerror')
g.write('888')
g.write('888')
g.write('0.1') # Percentage error to apply, in decimal form
g.write('onsource')
g.write('5')
g.write('setregions')
g.write('0')
g.write('specindex')
g.write('0')

#________________________________________________________
# Use BRATS to run the commands above
# Reference: https://github.com/JeremyHarwood/bratswrapper/blob/master/BRATS_Python_Wrapper/bratswapper_usageexample.py

import brats

# Bind the BRATS install location
spi_ = brats.Bind("/usr/bin/brats")

# Run multiple files in series with execfile():
spi_create = spi_.execfile("txt_files/spi_commands.txt")
print(spi_create)

