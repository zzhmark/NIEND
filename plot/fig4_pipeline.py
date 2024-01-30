# plotting for Figure 4

from utils.file_io import save_image
from v3dpy.loaders import PBD
from niend import *

from pathlib import Path
wkdir = Path(r'D:\rectify\fig')
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")


def pipeline(img_path: Path, sigma=10., pct=1, soma=(.5, .5, .5), win=(32, 128, 128), wavelet_levels=2):
    img = PBD().load(img_path)[0]

    temp = img.max(axis=0).clip(0, 65535).astype('uint16')
    save_image(wkdir / f"{img_path.name}_fig4_1.tiff", temp)

    win = np.array(win)
    img = img.astype(np.float32)
    diffusion_filter(img, sigma)

    orthogonal_filter(img)
    temp = img.max(axis=0).clip(0, 65535).astype('uint16')
    save_image(wkdir / f"{img_path.name}_fig4_2.tiff", temp)

    thr = np.percentile(img, 100 - pct)
    ct = (np.array(soma) * img.shape).astype(int)
    a = (ct - win // 2).clip(0)
    b = (ct + win // 2).clip(None, img.shape)
    high = min(255, img[a[0]:b[0], a[1]:b[1], a[2]:b[2]].max() * .5 - thr)
    img -= thr
    np.clip(img, 0, high, img)
    img /= high
    temp = (img * 255).max(axis=0).astype('uint8')
    save_image(wkdir / f"{img_path.name}_fig4_3.tiff", temp)

    wavelet_denoising(img, wavelet_levels)
    img = img_as_ubyte(img.clip(0, 1))
    temp = img.max(axis=0)
    save_image(wkdir / f"{img_path.name}_fig4_4.tiff", temp)


if __name__ == '__main__':

    pipeline(crop_path / '191801_15030_11091_4231.v3dpbd')