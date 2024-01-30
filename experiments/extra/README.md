# Extra experiments
Under this folder are the Scripts for running the extra experiments requested by reviewers.
Some of the experiments are run on 1891 neuronal blocks, which includes the 863 neurons used in this study.

## Folder structure
* `on_cluster`: scipts run on CentOS clusters.
  * `app1_1891.sh`: APP1 reconstruction on 1891 neuronal blocks
  * `app2_psf.sh`: APP2 reconstruction on R-L processed images
  * `gps_1891.sh`: NeuroGPS-Tree run on 1891 neuronal blocks
  * `psf.py`: constructing PSF and running R-L on a single image
  * `psf.sh`: for batch running psf.py on 1891 neuronal blocks
  * `psf_post.py`: for clearing the 6 faces of the R-L result to reduce over-tracing.
  * `psf_post.sh`: for batch running psf_post.py on 1891 blocks
  * `ultra_test.sh`: for running UltraTracer
* `app1_eval.py`: quantify the accuracy of APP1 results.
* `no_diffusion.py`: remove the diffusion filter, results will have more attenuation noise.
* `no_orthogonal.py`: remove the orthogonal filter, results will have more boundary artifacts.
* `no_high.py`: remove both the diffusion filter and the orthogonal filter, results will be very noisy.
* `no_shift.py`: remove intensity shifting, weak fibers will not be enhanced.
* `no_wvlet.py`: remove wavelet denoising, some of the images can be noisy with something like salt noise.
* `albation_eval.py`: quantify the accuracy of the tracing results.
* `instance_aware_test.py`: computing 0.5 max soma intensity for 1891 neurons 