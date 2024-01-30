# Experiments
Under this folder are the Scripts for running all the experiments.
Some of the experiments are run on 1891 neuronal blocks, which includes the 863 neurons used in this study.

## Folder structure
* `ablation`: ablation studies
* `extra`: experiments requested by reviewers
* `on_ubuntu`: scipts run on ubuntu workstation.
  * `ada_thr.py`: perform adaptive thresholding on 1891 images
  * `guo_enh.py`: perform Guo enhancement on 1891 images
  * `multiscale.py`: perform multiscale enhancment on 1891 images
  * `ubt_app2.py`: perform app2 on all the images
* `basic_app2.py`: perform app2 on raw and NIEND images
* `compress_lzma.py`: compress raw 8bit and NIEND images using LZMA
* `compress_multiscale.py`: compress multiscale enhancement images using v3dpbd
* `convert_raw_8bit.py`: convert 16bit raw images to 8bit
* `crop_gs.py`: crop gold standard neurons
* `crop_gs_profile.py`: crop gold standard neurons with profiled radius
* `diffusion_only.py`: perform only diffusion filtering on the images, for visualization
* `eval.py`: perform evaluation
* `filter.py`: perform NIEND on 1891 neuronal image blocks
* `masking.py`: use profiled neuron radius to create foreground and background masks, and extract the voxels
* `masking_stat.py`: use the masked voxels to compute image quality metrics
* `metadata_prep.py`: assemble all the metadata
* `thr_sampling.py`: perform APP2 thresholding on randomly sampled image blocks to analyze the image quality improvement
* `time_test.py`: test the time and memory usage of NIEND
* `highpass_only.py`: applying only high pass steps on 1891 neurons