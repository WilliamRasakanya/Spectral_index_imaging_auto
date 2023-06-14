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

TXT = cwd + '/txt_files/'
LOGS = cwd + '/txt_files/'

g = open(TXT + 'spi_commands.txt', 'w')
g.write('sigma')
g.write('5')
g.write('export')
g.write('exportasfits')
g.write('imageloc')
g.write('images')
g.write('load')
g.write('data')
g.write('noise.reg') # noise region
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
g.close()

#________________________________________________________
# Use BRATS to run the commands above
# Reference: https://github.com/JeremyHarwood/bratswrapper/blob/master/BRATS_Python_Wrapper/bratswapper_usageexample.py

import brats

h = open(LOGS + 'brats_logs.txt', 'w')
h.write('Running BRATS. \n')
h.write('BRATS python logs to appear here. \n \n')

# Bind the BRATS install location
spi_ = brats.Bind("/usr/bin/brats")

# Run multiple files in series with execfile():
spi_create = spi_.execfile(TXT+"spi_commands.txt")
#print(spi_create)
h.write(f'{spi_}' + '\n') # Returns a dictionary {file : returncode}. Returns 0 on success, else returns an error code.

# Alternatively, to have parallel runs with multiexec():
# files = ["./command1.txt", "./commands2.txt"] # List of command files
# runs_ = spi_.multiexec(files, 2) # Syntax: multiexec(list ["files", "to", "process"], int number_of_cores)
# print(runs_)
# h.write(f'{runs_}') # Returns a dictionary {commandfilename : returncode}. Returns 0 on success, else returns an error code.

h.close()
