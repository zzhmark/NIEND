# generate images
import skimage.io
from v3dpy.loaders import PBD
from pathlib import Path
from skimage.util import img_as_ubyte
from skimage.restoration import denoise_wavelet
from neuron_image_denoise.filter import *

def wavelet(img: np.ndarray):
    # img[...] = denoise_wavelet(img, mode='hard', wavelet_levels=2)
    for i in range(img.shape[0]):
        img[i] = denoise_wavelet(img[i], mode='hard', wavelet_levels=2)


def vertical_filter(img):
    mx = img.mean(axis=(0, 1))
    my = img.mean(axis=(0, 2))
    img -= np.add.outer(my, mx).astype(int)
    # for i in range(img.shape[1]):
    #     img[:, i, :] -= gaussian_filter(img[:,i,:], 32, truncate=2.)
    # for i in range(img.shape[2]):
    #     img[..., i] -= gaussian_filter(img[..., i], 32, truncate=2.)


wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")


if __name__ == '__main__':
    img = PBD().load(crop_path / "18464_21900_10258_5509.v3dpbd")[0]
    # PBD(pbd16_full_blood=False).save(wkdir / 'fig' / 'pipe0.v3dpbd', np.array([img]))
    skimage.io.imsave(wkdir / 'fig' / 'pipe0.tiff', img_as_ubyte(img.max(axis=0) / img.max()))

    img = img.astype(np.float32)
    adaptive_sectional_feedforward_filter(img, 12)
    # PBD(pbd16_full_blood=False).save(wkdir / 'fig' / 'pipe1.v3dpbd', np.array([img], dtype=np.uint16))
    skimage.io.imsave(wkdir / 'fig' / 'pipe1.tiff', img_as_ubyte(img.max(axis=0) / img.max()))

    vertical_filter(img)
    # PBD(pbd16_full_blood=False).save(wkdir / 'fig' / 'pipe2.v3dpbd', np.array([img], dtype=np.uint16))

    thr = np.percentile(img, 100 - 1)
    rescale_window = np.array([32, 128, 128])
    a = (img.shape - rescale_window) // 2
    b = (img.shape + rescale_window) // 2
    levels = min(255, (img[a[0]:b[0], a[1]:b[1], a[2]:b[2]].max() - thr) * .5)
    img -= thr
    np.clip(img, 0, levels, img)
    skimage.io.imsave(wkdir / 'fig' / 'pipe2.tiff', img_as_ubyte(img.max(axis=0) / img.max()))
    img /= levels
    wavelet(img)
    img = img_as_ubyte(img.clip(0, 1))
    skimage.io.imsave(wkdir / 'fig' / 'pipe3.tiff', img.max(axis=0))
