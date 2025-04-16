#!/usr/bin/env python
# coding: utf-8
__author__ = "William Rasakanya"
__copyright__ = "Copyright 2025"
__credits__ = ["William Rasakanya"]
__license__ = "GPL"
__email__ = "williamrasakanya.astro@gmail.com"

import os,sys
import argparse
import config

cwd = os.getcwd()
HOME = os.path.expanduser('~')


BIND = config.BIND
BINDPATH = config.BINDPATH

IDIA_CONTAINER_PATH = config.IDIA_CONTAINER_PATH
SLURM_CONTAINER_PATH = config.SLURM_CONTAINER_PATH
NODE_CONTAINER_PATH = config.NODE_CONTAINER_PATH

ASTROPY_PATTERN = config.ASTROPY_PATTERN
CASA_PATTERN = config.CASA_PATTERN
BRATS_PATTERN = config.BRATS_PATTERN

def make_executable(infile):

    mode = os.stat(infile).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(infile, mode)  

parser = argparse.ArgumentParser(description="Generate shell scripts for different platforms and methods")
parser.add_argument("platform", choices=["slurm", "node", "idia"], default="node", help="Target platform type")
parser.add_argument("method", nargs="?", default="brats", help="Execution method (e.g., brats, manual -- python)")

args = parser.parse_args()

platform = args.platform.lower()
method = args.method.lower()


if args.platform == "idia":
    s = config.SLURM_DEFAULTS

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
    g.write(f'#SBATCH --time={s["TIME"]}' + '\n')
    g.write(f'#SBATCH --partition={s["PARTITION"]}' + '\n')
    g.write(f'#SBATCH --ntasks={s["NTASKS"]}' + '\n')
    g.write(f'#SBATCH --nodes={s["NODES"]}' + '\n')
    g.write(f'#SBATCH --cpus-per-task={s["CPUS"]}' + '\n')
    g.write(f'#SBATCH --mem={s["MEM"]}' + '\n')
    g.write('SECONDS=0 \n')
    g.write('echo "Submitting Slurm job -- Beam info extraction"\n')
    g.write(f'singularity exec {IDIA_CONTAINER_PATH}{ASTROPY_PATTERN} python ' + cwd + '/beam_info_extraction.py \n')
    g.write('echo "****ELAPSED "$SECONDS" BeamExt \n"')
    g.close()

    make_executable(submit_file_beamext)

    submit_file_smooth = 'slurm_smooth_regrid.sh'

    g = open(submit_file_smooth, 'w')
    g.write('#!/usr/bin/bash' + '\n')
    g.write('\n')
    g.write('#SBATCH --job-name=SMOOTH' + '\n')
    g.write(f'#SBATCH --time={s["TIME"]}' + '\n')
    g.write(f'#SBATCH --partition={s["PARTITION"]}' + '\n')
    g.write(f'#SBATCH --ntasks={s["NTASKS"]}' + '\n')
    g.write(f'#SBATCH --nodes={s["NODES"]}' + '\n')
    g.write(f'#SBATCH --cpus-per-task={s["CPUS"]}' + '\n')
    g.write(f'#SBATCH --mem={s["MEM"]}' + '\n')
    g.write('SECONDS=0 \n')
    g.write('echo "Submitting Slurm job -- Automated image smoothing and regridding "\n')
    g.write(f'singularity exec {IDIA_CONTAINER_PATH}{CASA_PATTERN} casa -c ' + cwd + '/smooth_regrid.py'+ ' --log2term --nogui \n')
    g.write('echo "****ELAPSED "$SECONDS" SMOOTH"')
    g.close()

    make_executable(submit_file_smooth)

    submit_file_spi = 'slurm_spi.sh'

    g = open(submit_file_spi, 'w')
    g.write('#!/usr/bin/bash' +'\n')
    g.write('\n')
    g.write('#SBATCH --job-name=SPImap' + '\n')
    g.write(f'#SBATCH --time={s["TIME"]}' + '\n')
    g.write(f'#SBATCH --partition={s["PARTITION"]}' + '\n')
    g.write(f'#SBATCH --ntasks={s["NTASKS"]}' + '\n')
    g.write(f'#SBATCH --nodes={s["NODES"]}' + '\n')
    g.write(f'#SBATCH --cpus-per-task={s["CPUS"]}' + '\n')
    g.write(f'#SBATCH --mem={s["MEM"]}' + '\n')
    g.write('SECONDS=0 \n')
    if method == 'manual':
        g.write('# Generate spectral index map using custom code \n')
        g.write(f"singularity exec {IDIA_CONTAINER_PATH}{ASTROPY_PATTERN} python " + cwd + "/spi_gen_no_brats.py \n")
    elif method == 'brats':
        g.write('echo "Submitting Slurm job -- Spectral index map creation using BRATS "\n')
        g.write(f'DISPLAY="" singularity exec {IDIA_CONTAINER_PATH}{BRATS_PATTERN} python3 spi_map.py \n')
    g.write('echo "****ELAPSED "$SECONDS" SPImap"')
    g.close()

    make_executable(submit_file_spi)

elif args.platform == 'slurm':
    s = config.SLURM_DEFAULTS

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
    g.write(f'#SBATCH --time={s["TIME"]}' + '\n')
    g.write(f'#SBATCH --partition={s["PARTITION"]}' + '\n')
    g.write(f'#SBATCH --ntasks={s["NTASKS"]}' + '\n')
    g.write(f'#SBATCH --nodes={s["NODES"]}' + '\n')
    g.write(f'#SBATCH --cpus-per-task={s["CPUS"]}' + '\n')
    g.write(f'#SBATCH --mem={s["MEM"]}' + '\n')
    g.write('SECONDS=0 \n')
    g.write('echo "Submitting Slurm job -- Beam info extraction"\n')
    g.write(f'singularity exec {SLURM_CONTAINER_PATH}{ASTROPY_PATTERN} python ' + cwd + '/beam_info_extraction.py \n')
    g.write('echo "****ELAPSED "$SECONDS" BeamExt \n"')
    g.close()

    make_executable(submit_file_beamext)

    submit_file_smooth = 'slurm_smooth_regrid.sh'

    g = open(submit_file_smooth, 'w')
    g.write('#!/usr/bin/bash' + '\n')
    g.write('\n')
    g.write('#SBATCH --job-name=SMOOTH' + '\n')
    g.write(f'#SBATCH --time={s["TIME"]}' + '\n')
    g.write(f'#SBATCH --partition={s["PARTITION"]}' + '\n')
    g.write(f'#SBATCH --ntasks={s["NTASKS"]}' + '\n')
    g.write(f'#SBATCH --nodes={s["NODES"]}' + '\n')
    g.write(f'#SBATCH --cpus-per-task={s["CPUS"]}' + '\n')
    g.write(f'#SBATCH --mem={s["MEM"]}' + '\n')
    g.write('SECONDS=0 \n')
    g.write('echo "Submitting Slurm job -- Automated image smoothing and regridding "\n')
    g.write(f'singularity exec {SLURM_CONTAINER_PATH}{CASA_PATTERN} casa -c ' + cwd + '/smooth_regrid.py'+ ' --log2term --nogui \n')
    g.write('echo "****ELAPSED "$SECONDS" SMOOTH"')
    g.close()

    make_executable(submit_file_smooth)

    submit_file_spi = 'slurm_spi.sh'

    g = open(submit_file_spi, 'w')
    g.write('#!/usr/bin/bash' +'\n')
    g.write('\n')
    g.write('#SBATCH --job-name=SPImap' + '\n')
    g.write(f'#SBATCH --time={s["TIME"]}' + '\n')
    g.write(f'#SBATCH --partition={s["PARTITION"]}' + '\n')
    g.write(f'#SBATCH --ntasks={s["NTASKS"]}' + '\n')
    g.write(f'#SBATCH --nodes={s["NODES"]}' + '\n')
    g.write(f'#SBATCH --cpus-per-task={s["CPUS"]}' + '\n')
    g.write(f'#SBATCH --mem={s["MEM"]}' + '\n')
    g.write('SECONDS=0 \n')
    if method == 'manual':
        g.write('# Generate spectral index map using custom code \n')
        g.write(f"singularity exec {SLURM_CONTAINER_PATH}{ASTROPY_PATTERN} python " + cwd + "/spi_gen_no_brats.py \n")
    elif method == 'brats':
        g.write('echo "Submitting Slurm job -- Spectral index map creation using BRATS "\n')
        g.write(f'DISPLAY="" singularity exec {SLURM_CONTAINER_PATH}{BRATS_PATTERN} python3 spi_map.py \n')
    g.write('echo "****ELAPSED "$SECONDS" SPImap"')
    g.close()

    make_executable(submit_file_spi)

elif args.platform == 'node':

    submit_file = 'submit_spi_creation_job.sh'

    g = open(submit_file, 'w')
    g.write('#!/usr/bin/bash' +'\n\n')
    g.write('# Use python and astropy to find the right beam size from the list of images \n')
    g.write("python " + cwd + "/beam_info_extraction.py \n\n")
    g.write('# Use CASA to smooth the selected images \n')
    g.write("singularity exec " + NODE_CONTAINER_PATH + CASA_PATTERN + " casa -c " + cwd + "/smooth_regrid.py --log2term --nogui  \n\n")
    if method == 'manual':
        g.write('# Generate spectral index map using custom code \n')
        g.write("python " + cwd + "/spi_gen_no_brats.py \n")
    elif method == 'brats':
         g.write('# Generate spectral index map using BRATS \n')
         g.write('DISPLAY="" singularity exec '+ NODE_CONTAINER_PATH + BRATS_PATTERN + ' python3 spi_map.py ')
    g.close()

    make_executable(submit_file)

