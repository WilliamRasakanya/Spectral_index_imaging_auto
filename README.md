Created by William Rasakanya. An MSc Astrophysics student.

# Spectral_imaging_auto
A few python3 scripts to use in making spectral index images using radio image maps

The [automated_sh_generator_spix.py](https://github.com/WilliamRasakanya/Spectral_imaging_auto/blob/main/automated_sh_generator_spix.py) will generate three bash files which contain the required computing power inputs:
  - The "submit_smoothing_job.sh" bash file is the main bash file to be submitted on the terminal
  - The "slurm_astr3.sh" file is linked in the main submission file and it contains the instructions for the image beam info extraction 
  - The "slurm_casasmooth.sh" file will instruct the Common Astronomy Software Applications (CASA) package to smooth the required files to a resolution of an image with the largest beam size
 
 
