#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#****************Main file for an automated spectral index map maker***************


# Generate a bash file will submit a script that uses python:
#    to create folders, use astropy to get BMIN, BMAX etc. values

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

submit_file = 'submit_smoothing_job.sh'

g = open(submit_file, 'w')
g.write('#!/usr/bin/env bash \n')
g.write(' \n #---------------------------------------- \n')
g.write('\n # Use python and astropy to find the right beam size from the list of images')
g.write("\n Astr3beam=`sbatch " + cwd + "/slurm_astr3.sh | awk '{print $4}' `")
g.write('\n    ')
g.write('\n # Use CASA to smooth the selected images')
g.write("\n CASAsmooth=`sbatch -d afterok:${Astr3beam} " + cwd + "/slurm_casasmooth.sh | awk '{print $4}' `")
g.close()

make_executable(submit_file) # From Ian Heywood GitHub

submit_file_astr3 = 'slurm_astr3.sh'

g = open(submit_file_astr3, 'w')
g.write('#!/usr/bin/bash' + '\n')
g.write('\n')
g.write('#SBATCH --job-name=AP3beamInfo' + '\n')
g.write('#SBATCH --time=12:00:00' + '\n')
g.write('#SBATCH --partition=Main' + '\n')
g.write('#SBATCH --ntasks=1' + '\n')
g.write('#SBATCH --nodes=1' + '\n')
g.write('#SBATCH --cpus-per-task=8' + '\n')
g.write('#SBATCH --mem=64GB' + '\n')
g.write('SECONDS=0')
g.write('\n echo "Submitting Slurm job -- Beam info extraction using astropy"')
g.write('\n singularity exec /idia/software/containers/ASTRO-PY3.simg python ' + cwd + '/beam_info_extraction.py')
g.write('\n echo "****ELAPSED "$SECONDS" PY3-Astro"')
g.close()

make_executable(submit_file_astr3)

submit_file_casa = 'slurm_casasmooth.sh'

g = open(submit_file_casa, 'w')
g.write('#!/usr/bin/bash' + '\n')
g.write('\n')
g.write('#SBATCH --job-name=CASAsmoothing' + '\n')
g.write('#SBATCH --time=12:00:00' + '\n')
g.write('#SBATCH --partition=Main' + '\n')
g.write('#SBATCH --ntasks=1' + '\n')
g.write('#SBATCH --nodes=1' + '\n')
g.write('#SBATCH --cpus-per-task=8' + '\n')
g.write('#SBATCH --mem=64GB' + '\n')
g.write('SECONDS=0')
g.write('\n echo "Submitting Slurm job -- Automated CASA smoothing"')
g.write('\n singularity exec /idia/software/containers/casa-stable.img casa -c ' + cwd + '/casa_smoothing.py'+ ' --log2term --nogui')
g.write('\n echo "****ELAPSED "$SECONDS" CASA_smoothing"')
g.close()

make_executable(submit_file_casa) 


