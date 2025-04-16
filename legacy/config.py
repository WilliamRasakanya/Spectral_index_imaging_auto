import os
import sys

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
# cannot see by default then set BIND to that path.
# If you wish to bind multiple paths then use a comma-separated list.
BIND = ''
BINDPATH = '$PWD,'+CWD+','+BIND

IDIA_CONTAINER_PATH = ['/idia/software/containers/',HOME+'/containers/']
CHPC_CONTAINER_PATH = [HOME+'/containers/']
HIPPO_CONTAINER_PATH = None
NODE_CONTAINER_PATH = [HOME+'/software/containers/']


ASTROPY_PATTERN = 'ASTRO-PY3.simg'
CASA_PATTERN = 'casa-stable.img'
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

