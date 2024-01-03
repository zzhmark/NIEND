import numpy as np
from skimage.util import img_as_ubyte
from v3dpy.loaders import PBD
from skimage.restoration import denoise_wavelet
from skimage.filters import gaussian
from skimage.transform import rescale, downscale_local_mean
import functools


def wavelet_denoising(img: np.ndarray, wavelet_levels):
    for i in range(img.shape[0]):
        img[i] = denoise_wavelet(img[i], mode='hard', wavelet_levels=wavelet_levels)


def orthogonal_filter(img):
    mx = img.mean(axis=(0, 1))
    my = img.mean(axis=(0, 2))
    img -= np.add.outer(my, mx).astype(int)


def diffusion_filter(img: np.ndarray, sigma=10., truncate=3., scaling=1, suppression=.8):
    """
    cancel flare and background noise. More adaptive canceling, and its effect can be tuned.

    :param img: 3D image array.
    :param sigma: gaussian sigma, scalar or a tuple of 2 scalar.
    :param truncate: this many times of sigma will be truncated to speed up gaussian.
    :param scaling: downsampling times to speed up.
    :param suppression: 0-1, suppress the canceling effect.
    :return: processed image
    """
    diffuse = functools.partial(gaussian, sigma=sigma / scaling, preserve_range=True, truncate=truncate)
    downscale = functools.partial(downscale_local_mean, factors=scaling)
    upscale = functools.partial(rescale, scale=scaling)

    out = np.zeros_like(img)
    gpool = diffuse(downscale(img[-1]))
    for i in range(1, img.shape[0]):
        i = img.shape[0] - i - 1
        m = img[i].mean() / gpool.mean() * suppression
        out[i] = (img[i] - upscale(m * gpool)).clip(0)
        gpool = diffuse(downscale(out[i]) + gpool)
    return out


def standard_niend(img: np.ndarray, sigma=10., pct=.01, win=(32, 128, 128), wavelet_levels=2):
    win = np.array(win)
    img = img.astype(np.float32)
    diffusion_filter(img, sigma)
    orthogonal_filter(img)
    thr = np.percentile(img, 100 - pct)
    a = (img.shape - win) // 2
    b = (img.shape + win) // 2
    levels = min(255, (img[a[0]:b[0], a[1]:b[1], a[2]:b[2]].max() - thr) * .5)
    img -= thr
    np.clip(img, 0, levels, img)
    img /= levels
    wavelet_denoising(img, wavelet_levels)
    img = img_as_ubyte(img.clip(0, 1))
    return img


def simple_niend(img: np.ndarray, sigma=10., pct=.01, wavelet_levels=2):
    """
    No instance awareness, just retain at most 256 grayscales

    :param img:
    :param sigma:
    :param pct: determining lowerbound.
    :return:
    """
    img = img.astype(np.float32)
    diffusion_filter(img, sigma)
    orthogonal_filter(img)
    img -= np.percentile(img, 100 - pct)
    np.clip(img, 0, 255, img)
    img /= 255
    wavelet_denoising(img, wavelet_levels)
    img = img_as_ubyte(img.clip(0, 1))
    return img