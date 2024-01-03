# my new method

from pathlib import Path
from multiprocessing import Pool
from skimage.util import img_as_ubyte

import pandas as pd
from v3dpy.loaders import PBD
from neuron_image_denoise.filter import *
from tqdm import tqdm
from skimage.restoration import denoise_wavelet
from memory_profiler import profile
import time

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
# out_dir = wkdir / 'my'


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


# @profile
def main(args):
    in_path, sigma, pct = args
    rescale_window = np.array([32, 128, 128])
    # out_path = out_dir / in_path.name
    # if out_path.exists():
    #     return
    img = PBD().load(in_path)[0,:,384:640,384:640].astype(np.float32)
    t1 = time.time()
    adaptive_sectional_feedforward_filter(img, sigma)
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
    t2 = time.time()
    # print(t2 - t1)
    return t2 - t1
    # PBD().save(out_path, img.reshape(1, *img.shape))


if __name__ == '__main__':
    s_tab = pd.read_csv(wkdir / 'param.csv', index_col=0)
    # out_dir.mkdir(exist_ok=True)
    arglist = []
    for f in crop_path.rglob('*.v3dpbd'):
        brain = int(f.name.split('_')[0])
        arglist.append((f, s_tab.at[brain, 'sigma'], s_tab.at[brain, 'pct']))

    # main((crop_path / "17545_21113_13119_3782.v3dpbd", 12, 1))
    from random import sample
    arglist = sample(arglist, 30)

    tt = []
    with Pool(1) as p:
        for t in tqdm(p.imap(main, arglist), total=len(arglist)):
            tt.append(t)
    tt = tt[10:]
    import pickle
    with open(wkdir / f'time_use_256.pickle', 'wb') as f:
        pickle.dump(tt, f)

