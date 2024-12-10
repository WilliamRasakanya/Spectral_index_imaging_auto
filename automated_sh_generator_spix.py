#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#****************Main file for an automated spectral index map creator***************


# Generate a bash file will submit a script that uses python:
#    to create folders, use astropy to get BMIN, BMAJ etc. values

import os,sys

cwd = os.getcwd()
HOME = os.path.expanduser('~')

# ------------------------------------------------------------------------
# From Ian Heywood oxkat github: https://github.com/IanHeywood/oxkat/
#
# Singularity settings
#

# Bind the symlinked location of the input image files.
BIND = ''
BINDPATH = '$PWD,'+cwd+','+BIND

NODE_CONTAINER_PATH = HOME+'/software/containers/'

CASA = 'oxkat-0.41.sif'
BRATS = 'kern6.simg'

# ------------------------------------------------------------------------

# define how the method and machine to run the pipeline on

def get_input(s, default=None):
    try:
        i = sys.argv.index(s)
        return sys.argv[i+1]
    except (ValueError, IndexError):
        return None

# machine = get_input(1, "node") # Work in progress
machine = 'node' # Change this to 'idia' if you want ilifu-type bash submission on a slurm scheduler
spi_method = get_input(2, 'manual') # Change this to 'brats' if you want to use brats. You will need to edit the spi_map.py file for redshift, and will need a noise ds9 region file

# ------------------------------------------------------------------------

def make_executable(infile):

    # https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python

    mode = os.stat(infile).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(infile, mode)    

    
    if machine == 'node' or None: 

        submit_file = 'submit_spi_creation_job.sh'
        
        g = open(submit_file, 'w')
        g.write('#!/usr/bin/bash' +'\n\n')
        g.write('# Use python and astropy to find the right beam size from the list of images \n')
        g.write("python " + cwd + "/beam_info_extraction.py \n\n")
        g.write('# Use CASA to smooth the selected images \n')
        g.write("singularity exec " + NODE_CONTAINER_PATH + CASA + " casa -c " + cwd + "/smooth_regrid.py --log2term --nogui  \n\n")
        if spi_method == 'manual' or None:
            g.write('# Generate spectral index map using custom code \n')
            g.write("python " + cwd + "/spec_index_z_absent.py \n")
        elif spi_method == 'brats':
             g.write('# Generate spectral index map using BRATS \n')
             g.write('singularity exec '+ NODE_CONTAINER_PATH + BRATS + ' python3 spi_map.py ')
        g.close()

        make_executable(submit_file)

    elif machine == 'idia':

        submit_file = 'submit_spi_creation_job.sh'
    
        g = open(submit_file, 'w')
        g.write('#!/usr/bin/env bash \n')
        g.write(' \n#---------------------------------------- \n\n')
        g.write('# Use python and astropy to find the right beam size from the list of images \n')
        g.write("BeamExt=`sbatch " + cwd + "/slurm_beamext.sh | awk '{print $4}' `\n")
        g.write('\n    \n')
        g.write('# Use CASA to smooth the selected images \n')
        g.write("SMOOTH=`sbatch -d afterok:${BeamExt} " + cwd + "/slurm_smooth_regrid.sh | awk '{print $4}' ` \n")
        g.write('\n    \n')
        g.write('# Use BRATS to create a spectral index map \n')
        g.write("SPImap=`sbatch -d afterok:${SMOOTH} " + cwd + "/slurm_spi.sh | awk '{print $4}' `")
        g.close()

        make_executable(submit_file) 
    
        submit_file_beamext = 'slurm_beamext.sh'
    
        g = open(submit_file_beamext, 'w')
        g.write('#!/usr/bin/bash' + '\n')
        g.write('\n')
        g.write('#SBATCH --job-name=BeamExt' + '\n')
        g.write('#SBATCH --time=12:00:00' + '\n')
        g.write('#SBATCH --partition=Main' + '\n')
        g.write('#SBATCH --ntasks=1' + '\n')
        g.write('#SBATCH --nodes=1' + '\n')
        g.write('#SBATCH --cpus-per-task=8' + '\n')
        g.write('#SBATCH --mem=64GB' + '\n')
        g.write('SECONDS=0 \n')
        g.write('echo "Submitting Slurm job -- Beam info extraction using astropy \n"')
        g.write('singularity exec /idia/software/containers/ASTRO-PY3.simg python ' + cwd + '/beam_info_extraction.py \n')
        g.write('echo "****ELAPSED "$SECONDS" BeamExt \n"')
        g.close()
    
        make_executable(submit_file_beamext)
    
        submit_file_smooth = 'slurm_smooth_regrid.sh'
    
        g = open(submit_file_smooth, 'w')
        g.write('#!/usr/bin/bash' + '\n')
        g.write('\n')
        g.write('#SBATCH --job-name=SMOOTH' + '\n')
        g.write('#SBATCH --time=12:00:00' + '\n')
        g.write('#SBATCH --partition=Main' + '\n')
        g.write('#SBATCH --ntasks=1' + '\n')
        g.write('#SBATCH --nodes=1' + '\n')
        g.write('#SBATCH --cpus-per-task=8' + '\n')
        g.write('#SBATCH --mem=64GB' + '\n')
        g.write('SECONDS=0 \n')
        g.write('echo "Submitting Slurm job -- Automated image smoothing and regridding \n"')
        g.write('singularity exec /idia/software/containers/casa-stable.img casa -c ' + cwd + '/smooth_regrid.py'+ ' --log2term --nogui \n')
        g.write('echo "****ELAPSED "$SECONDS" SMOOTH"')
        g.close()
    
        make_executable(submit_file_smooth) 
    
        # From Jeremy Harwood GitHub
        # https://github.com/JeremyHarwood/bratswrapper
    
        submit_file_spi = 'slurm_spi.sh'
    
        g = open(submit_file_spi, 'w')
        g.write('#!/usr/bin/bash' +'\n')
        g.write('\n')
        g.write('#SBATCH --job-name=SPImap' + '\n')
        g.write('#SBATCH --time=12:00:00' + '\n')
        g.write('#SBATCH --partition=Main' + '\n')
        g.write('#SBATCH --ntasks=1' + '\n')
        g.write('#SBATCH --nodes=1' + '\n')
        g.write('#SBATCH --cpus-per-task=8' + '\n')
        g.write('#SBATCH --mem=128GB' + '\n')
        g.write('SECONDS=0 \n')
        if spi_method == 'manual':
            g.write('# Generate spectral index map using custom code \n')
            g.write("singularity exec /idia/software/containers/ASTRO-PY3.simg python " + cwd + "/spec_index_z_absent.py \n")
        elif spi_method == 'brats':
            g.write('echo "Submitting Slurm job -- Spectral index map creation using BRATS \n"')
            g.write('singularity exec /idia/software/containers/kern6.simg python3 spi_map.py \n')
        g.write('echo "****ELAPSED "$SECONDS" SPImap"')
        g.close()
    
        make_executable(submit_file_spi)



