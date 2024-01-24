# Ablation Study
Under this folder are the Python Scripts for running the ablation study, which removes each of the steps in NIEND
and reconstruct the neuron using APP2.

## Folder structure
* 8bit: set the input as 8bit rather than 16bit, this shows the significance of using the 16bit images.
NIEND is mostly powerful for dealing with the high-depth images.
* no_diffusion: remove the diffusion filter, results will have more attenuation noise.
* no_orthogonal: remove the orthogonal filter, results will have more boundary artifacts.
* no_high: remove both the diffusion filter and the orthogonal filter, results will be very noisy.
* no_shift: remove intensity shifting, weak fibers will not be enhanced.
* no_wvlet: remove wavelet denoising, some of the images can be noisy with something like salt noise.
* albation_eval: quantify the accuracy of the tracing results.