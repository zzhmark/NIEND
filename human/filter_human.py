# filter for human
from pathlib import Path
from multiprocessing import Pool
from skimage.util import img_as_ubyte

from v3dpy.loaders import PBD
from neuron_image_denoise.filter import *
from tqdm import tqdm
from skimage.restoration import denoise_wavelet
from img_pca_filter import img_pca_test
import subprocess


wkdir = Path(r"D:\rectify")
crop_path = wkdir / 'human_crop'


def main(args):
    in_path = args
    rescale_window = np.array([64, 64, 64])
    out_path = wkdir / 'my_human' / in_path.name
    if out_path.exists():
        return
    p = PBD()
    img = p.load(in_path)[0].astype(np.uint16)
    s = img.shape
    pw = (s[0] // 4 + 1) * 4 - s[0]
    t = np.pad(img, ((0, pw), (0, 0), (0, 0)), 'reflect').astype(np.uint16)
    t = img_pca_test(t, (8, 8, 8), (4, 4, 4))[:s[0]]
    img = adaptive_denoise(img, (2, 2, 2), ada_sampling=3, flare_sampling=0)
    img = gaussian(img, 1, preserve_range=True) * t
    thr = np.percentile(img, 100 - 5)
    a = (img.shape - rescale_window) // 2
    b = (img.shape + rescale_window) // 2
    levels = min(255, (img[a[0]:b[0], a[1]:b[1], a[2]:b[2]].max() - thr) * .5)
    img -= thr
    np.clip(img, 0, levels, img)
    img /= levels
    img = img_as_ubyte(img.clip(0, 1))
    PBD(pbd16_full_blood=False).save(out_path, img.reshape(1, *img.shape))
    subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {out_path} /p no 0 AUTO 0 0 1 0 1 1 0 0', stdout=subprocess.DEVNULL)


if __name__ == '__main__':
    arglist = []
    for f in crop_path.rglob('*.v3dpbd'):
        arglist.append(f)

    with Pool(12) as p:
        for res in tqdm(p.imap(main, arglist), total=len(arglist)): pass


