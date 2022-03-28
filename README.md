Created by William Rasakanya. An MSc Astrophysics student.

---

## Spectral_imaging_auto
A few python3 scripts to use in making spectral index images using radio image maps

The [automated_sh_generator_spix.py](https://github.com/WilliamRasakanya/Spectral_imaging_auto/blob/main/automated_sh_generator_spix.py) will generate three bash files which contain the required computing power inputs:
  * The "submit_smoothing_job.sh" bash file is the main bash file to be submitted on the terminal
  * The "slurm_astr3.sh" file is linked in the main submission file and it contains the instructions for the image beam info extraction 
  * The "slurm_casasmooth.sh" file will instruct the Common Astronomy Software Applications (CASA) package to smooth the required files to a resolution of an image with the largest beam size
 
 ---
 
 ## Quick start
 1. ssh into your machine or cluster, e.g.:
    ```
    $ ssh username@slurm.clustername.ac.cc
    ```
 2. Navigate to an empty, working area:
    ```
    $ cd path/to/empty_folder
    ```
 3. Clone the root contents of this repo into it:
    ```
    $ git clone https://github.com/WilliamRasakanya/Spectral_imaging_auto.git .
    ```
 4. Make a symlink to your .fits images or copy them to the current directory
    ```
    $ ln -s path/to/fitsfile/file.fits .
    ```
    OR
    ```
    $ cp path/to/fitsfile/file.fits .
    ```
 5. Generate the bash submission files
    ```
    $ python  automated_sh_generator_spix.py idia
    ```
 6. Write or copy the background (noise) region (DS9 format or otherwise{untested}) to the /noise directory
 7. Submit the job:
    ``` 
    $ ./submit_smoothing_job.sh
    ```
 
 More info might be added in the future as my skills improve.
 
 Thank you and I hope this assists you in some capacity.
