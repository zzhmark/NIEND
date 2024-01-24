from skimage.restoration import richardson_lucy
from v3dpy.loaders import PBD
from pathlib import Path
import sys
import numpy as np
from scipy.stats import norm, skewnorm
from scipy.signal.windows import gaussian

def create_asymmetric_psf(size_xy, size_z, sigma_xy, sigma_z, skewness):
    # Create a 3D grid
    z, y, x = np.ogrid[-size_z//2:size_z//2, -size_xy//2:size_xy//2, -size_xy//2:size_xy//2]

    # Calculate the Gaussian distribution in the xy plane
    g = np.outer(gaussian(size_xy, sigma_xy), gaussian(size_xy, sigma_xy))
    gaussian_xy = np.repeat(g[np.newaxis, :, :], size_z, axis=0)

    # Calculate the skewed normal distribution in the z direction
    skewnorm_z = skewnorm.pdf(z, skewness, scale=sigma_z)

    # Multiply the two distributions to get the final PSF
    psf = gaussian_xy * skewnorm_z

    return psf / psf.sum()



if __name__ == '__main__':
    from multiprocessing import Pool
    in_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    img = PBD().load(in_path)[0].astype('float32')
    img /= img.max()
    outpath = out_dir / in_path.name
    if outpath.exists():
        exit()

    psf = create_asymmetric_psf(10, 20, 2, 5, -5)
    img = 1 - richardson_lucy(img, psf, num_iter=30)
    
    m1, m2 = img.max(), img.min()
    img = ((img - m1) * (255 / (m2 - m1))).astype('uint8')
    PBD().save(outpath, img.reshape([1, *img.shape]))
    
    