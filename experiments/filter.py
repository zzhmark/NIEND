# my new method

from pathlib import Path
from multiprocessing import Pool
from skimage.util import img_as_ubyte

import pandas as pd
from v3dpy.loaders import PBD
from neuron_image_denoise.filter import *
from tqdm import tqdm
from skimage.restoration import denoise_wavelet

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'my'


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


def main(args):
    in_path, sigma, pct = args
    rescale_window = np.array([32, 128, 128])
    out_path = out_dir / in_path.name
    if out_path.exists():
        return
    p = PBD()
    img = p.load(in_path)[0].astype(np.float32)
    adaptive_sectional_feedforward_filter(img, sigma, suppression=.8)
    vertical_filter(img)
    thr = np.percentile(img, 100 - pct)
    a = (img.shape - rescale_window) // 2
    b = (img.shape + rescale_window) // 2
    levels = min(255, (img[a[0]:b[0], a[1]:b[1], a[2]:b[2]].max() - thr) * .5)
    img -= thr
    np.clip(img, 0, levels, img)
    img /= levels
    wavelet(img)
    img = img_as_ubyte(img.clip(0, 1))
    PBD().save(out_path, img.reshape(1, *img.shape))


if __name__ == '__main__':
    s_tab = pd.read_csv(wkdir / 'param.csv', index_col=0)
    out_dir.mkdir(exist_ok=True)
    arglist = []
    for f in crop_path.rglob('*.v3dpbd'):
        brain = int(f.name.split('_')[0])
        arglist.append((f, s_tab.at[brain, 'sigma'], s_tab.at[brain, 'pct']))

    main((r"C:\Users\zzh\Downloads\0011.tiff", 12, 1))

    # with Pool(12) as p:
    #     for res in tqdm(p.imap(main, arglist), total=len(arglist)): pass

