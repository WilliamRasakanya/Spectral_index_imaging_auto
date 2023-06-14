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
g.write('sigma' + '\n')
g.write('5' + '\n')
g.write('export' + '\n')
g.write('exportasfits' + '\n')
g.write('imageloc' + '\n')
g.write('images' + '\n')
g.write('load' + '\n')
g.write('data' + '\n')
g.write('noise.reg' + '\n') # noise region
g.write('txt_files/full_map.reg' + '\n') # region file path (Default will use the full map)
g.write('0.0474' + '\n') # redshift of the source of interest
g.write('specindexcalctype' + '\n')
g.write('2' + '\n')
g.write('fluxcalerror' + '\n')
g.write('888' + '\n')
g.write('888' + '\n')
g.write('0.1' + '\n') # Percentage error to apply, in decimal form
g.write('onsource' + '\n')
g.write('5' + '\n')
g.write('setregions' + '\n')
g.write('0' + '\n')
g.write('specindex' + '\n')
g.write('0' + '\n')
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
