import numpy as np
from skimage.util import img_as_ubyte
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


def diffusion_filter(img: np.ndarray, sigma=10., truncate=2., suppression=.9):
    """
    cancel flare and background noise. More adaptive canceling, and its effect can be tuned.

    :param img: 3D image array.
    :param sigma: gaussian sigma, scalar or a tuple of 2 scalar.
    :param truncate: this many times of sigma will be truncated to speed up gaussian.
    :param scaling: downsampling times to speed up.
    :param suppression: 0-1, suppress the canceling effect.
    :return: processed image
    """
    diffuse = functools.partial(gaussian, sigma=sigma, preserve_range=True, truncate=truncate)

    gpool = diffuse(img[-1])
    for i in range(img.shape[0]):
        i = img.shape[0] - i - 1
        m1, m2 = img[i].mean(), gpool.mean()
        if m2 == 0:
            m = suppression
        else:
            m = m1 / m2 * suppression
        img[i] = (img[i] - m * gpool).clip(0)
        gpool = diffuse(img[i] + gpool)


def standard_niend(img: np.ndarray, sigma=10., pct=1, soma=(.5, .5, .5), win=(32, 128, 128), wavelet_levels=2):
    win = np.array(win)
    img = img.astype(np.float32)
    diffusion_filter(img, sigma)
    orthogonal_filter(img)
    thr = np.percentile(img, 100 - pct)
    ct = (np.array(soma) * img.shape).astype(int)
    a = (ct - win // 2).clip(0)
    b = (ct + win // 2).clip(None, img.shape)

    high = min(255, img[a[0]:b[0], a[1]:b[1], a[2]:b[2]].max() * .5 - thr)
    img -= thr
    np.clip(img, 0, high, img)
    img /= high
    wavelet_denoising(img, wavelet_levels)
    img = img_as_ubyte(img.clip(0, 1))
    return img


def simple_niend(img: np.ndarray, sigma=10., pct=1, wavelet_levels=2):
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