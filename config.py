#!/usr/bin/env python
# coding: utf-8
__author__ = "William Rasakanya"
__copyright__ = "Copyright 2025"
__credits__ = ["William Rasakanya"]
__license__ = "GPL"
__email__ = "williamrasakanya.astro@gmail.com"

import os,sys

# ------------------------------------------------------------------------
#
# Paths for components and OUTPUTS
#

CWD = os.getcwd()
HOME = os.path.expanduser('~')


# ------------------------------------------------------------------------
#
# Singularity settings
#

# Set to False to disable singularity entirely
USE_SINGULARITY = True

# If your data are symlinked and located in a path that singularity
# cannot see by default (e.g. data in a mount '/mnt/') then set BIND to that path.
# If you wish to bind multiple paths then use a comma-separated list.
BIND = ''
BINDPATH = '$PWD,'+CWD+','+BIND

IDIA_CONTAINER_PATH = '/idia/software/containers/'
SLURM_CONTAINER_PATH = HOME+'/containers/'
NODE_CONTAINER_PATH = HOME+'/software/containers/'

# Container names.
ASTROPY_PATTERN = 'ASTRO-PY3.10.sif' # Can change this to any container with astropy installed.
CASA_PATTERN = 'casa-stable.img' # Can change this to any CASA container you need to use.
BRATS_PATTERN = 'kern6.simg'

# ------------------------------------------------------------------------
#
# Slurm resource settings
#

SLURM_DEFAULTS = {
	'TIME': '12:00:00',
	'PARTITION': 'Main',
	'NTASKS': '1',
	'NODES': '1',
	'CPUS': '8',
	'MEM': '64GB',
}

