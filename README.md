Created by William Rasakanya. A PhD Astrophysics student at the University of the Witwatersrand.

---

## Spectral_index_imaging_auto
A few `Python` scripts to use to create spectral index (and age) images using radio images.

The [automated_sh_generator.py](https://github.com/WilliamRasakanya/Spectral_imaging_auto/blob/main/automated_sh_generator.py), when using BRATS as the method for spectral index map generation, will generate four bash files (which contain the required computing power inputs):
  * The "submit_spi_creation_job.sh" bash file is the main bash file to be submitted on the terminal.
  * The "slurm_beamext.sh" file is linked in the main submission file and it contains the instructions for the image beam info extraction and creates a _physical_ full map region file. If no noise.reg file is in main folder, [noise_calc.py](noise_calc.py) will generate a noise.reg region file automatically.
  * The "slurm_smooth_regrid.sh" file will instruct the Common Astronomy Software Applications (`CASA`) package to smooth and regrid the required files to a resolution of an image with the largest beam size.
  * Finally, the "slurm_spi.sh" file will use the Broadband Radio Astronomy Tools (`BRATS`) software to create a spectral index map. Thereafter, a copy of the output image will be made, with its coordinates fixed to align with those of the input images.
  * [spi_commands.txt](spi_commands.txt) contains BRATS commands in the required order ([BRATS cookbook](https://askanastronomer.co.uk/brats/downloads/bratscookbook.pdf)). Modify as needed. Additional BRATS commands can be added.

An alternative and flexible method to use is the 'manual' one, which uses a custom python code and implements the definition of spectral index on a pixel-by-pixel basis. No  redshift info required.

NB: Ensure that all the input images have the same angular sizes and the same sky coordinates, and that they are square-shaped (only for BRATS).

 ---
 
 ## Quick start
 1. ssh into your machine or cluster, e.g.:
    ```
    ssh username@slurm.clustername.ac.cc
    ```
 2. Navigate to an empty, working area:
    ```
    cd path/to/empty_folder
    ```
 3. Clone the root contents of this repo into it:
    ```
    git clone https://github.com/WilliamRasakanya/Spectral_imaging_auto.git .
    ```
 4. Make a symlink to your .fits images or copy them to the current directory
    ```
    ln -s path/to/fitsfile/file.fits .
    ```
    OR
    ```
    cp path/to/fitsfile/file.fits .
    ```
 5. (Optional) Write or copy the background (noise) region (DS9 format) to the current directory, with name noise.reg
    ```
    ln -s path/to/noisefile/noise.reg .
    ```
    OR
    ```
    cp path/to/noisefile/noise.reg .
    ```
 6. Generate the bash submission files <br /> &emsp;
     Specify the machine to run on and the method of spectral index generation: <br /> &emsp;&emsp;
     Machine: 'node'/None, 'idia', 'slurm'.    Method: 'brats'/None or 'manual'. 
    ```
    python automated_sh_generator.py
    ```
 8. Submit the job:
    ``` 
    ./submit_spi_creation_job.sh
    ```
 
 
 ---
 
 ## Containers
 
 These sets of scripts run the following software packages:
 * [`CASA`](https://casa.nrao.edu/): To smooth the images to the resolution of the image with the largest beam size.
   * Reference: [McMullin et al., 2007](https://ui.adsabs.harvard.edu/abs/2007ASPC..376..127M/abstract)
 
 * [`BRATS`](http://www.askanastronomer.co.uk/brats/): To create radio spectral index maps (and various others, eg. Spectral Age maps).
   * Reference: [Harwood et al., 2013, MNRAS, 435, 3353](http://mnras.oxfordjournals.org/content/435/4/3353); [Harwood et al., 2015, MNRAS, 454, 3403](http://mnras.oxfordjournals.org/content/454/4/3403)
  
 * [`bratswrapper`](https://github.com/JeremyHarwood/bratswrapper): [@JeremyHarwood](https://github.com/JeremyHarwood)'s `Python` wrapper which allows for automation of the process.
 ---
 
 More info might be added in the future as my skills improve.
 
 Thank you and I hope this assists you in some capacity.
