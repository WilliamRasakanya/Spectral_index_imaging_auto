#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#****************Main file for an automated spectral index map creator***************


# Generate a bash file will submit a script that uses python:
#    to create folders, use astropy to get BMIN, BMAJ etc. values

import os

cwd = os.getcwd()

#*******************************************
# From Ian Heywood GitHub
# https://github.com/IanHeywood/oxkat

def make_executable(infile):

    # https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python

    mode = os.stat(infile).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(infile, mode)    

    
awk_arg = '{print $4}'    

submit_file = 'submit_spi_creation_job.sh'

g = open(submit_file, 'w')
g.write('#!/usr/bin/env bash \n')
g.write(' \n #---------------------------------------- \n')
g.write('\n # Use python and astropy to find the right beam size from the list of images')
g.write("\n BeamExt=`sbatch " + cwd + "/slurm_beamext.sh | awk '{print $4}' `")
g.write('\n    ')
g.write('\n # Use CASA to smooth the selected images')
g.write("\n SMOOTH=`sbatch -d afterok:${BeamExt} " + cwd + "/slurm_casasmooth.sh | awk '{print $4}' `")
g.write('\n    ')
g.write('\n # Use BRATS to create a spectral index map')
g.write("\n SPImap=`sbatch -d afterok:${SMOOTH} " + cwd + "/slurm_spi.sh | awk '{print $4}' `")
g.close()

make_executable(submit_file) # From Ian Heywood GitHub

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
g.write('SECONDS=0')
g.write('\n echo "Submitting Slurm job -- Beam info extraction using astropy"')
g.write('\n singularity exec /idia/software/containers/ASTRO-PY3.simg python ' + cwd + '/beam_info_extraction.py')
g.write('\n echo "****ELAPSED "$SECONDS" BeamExt"')
g.close()

make_executable(submit_file_beamext)

submit_file_casa = 'slurm_casasmooth.sh'

g = open(submit_file_casa, 'w')
g.write('#!/usr/bin/bash' + '\n')
g.write('\n')
g.write('#SBATCH --job-name=SMOOTH' + '\n')
g.write('#SBATCH --time=12:00:00' + '\n')
g.write('#SBATCH --partition=Main' + '\n')
g.write('#SBATCH --ntasks=1' + '\n')
g.write('#SBATCH --nodes=1' + '\n')
g.write('#SBATCH --cpus-per-task=8' + '\n')
g.write('#SBATCH --mem=64GB' + '\n')
g.write('SECONDS=0')
g.write('\n echo "Submitting Slurm job -- Automated CASA smoothing"')
g.write('\n singularity exec /idia/software/containers/casa-stable.img casa -c ' + cwd + '/casa_smoothing.py'+ ' --log2term --nogui')
g.write('\n echo "****ELAPSED "$SECONDS" SMOOTH"')
g.close()

make_executable(submit_file_casa) 

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
g.write('SECONDS=0')
g.write('\n echo "Submitting Slurm job -- Spectral index map creation using BRATS"')
g.write('\n singularity exec /idia/software/containers/kern6.simg python3 ' + cwd + 'spi_map.py')
g.write('\n echo "****ELAPSED "$SECONDS" SPImap"')
g.close()

make_executable(submit_file_spi)


