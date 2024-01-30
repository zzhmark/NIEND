# applying only high pass steps

from pathlib import Path
from multiprocessing import Pool

import pandas as pd
from v3dpy.loaders import PBD
from niend import *
from tqdm import tqdm

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'highpass_only'

def niend(img: np.ndarray, sigma=10., pct=1, soma=(.5, .5, .5), win=(32, 128, 128), wavelet_levels=2):
    win = np.array(win)
    img = img.astype(np.float32)
    diffusion_filter(img, sigma)
    orthogonal_filter(img)
    np.clip(img, 0, None, img)
    img = img.astype('uint16')
    return img


def main(args):
    in_path, sigma, pct = args
    out_path = out_dir / in_path.name
    if out_path.exists():
        return
    p = PBD()
    img = p.load(in_path)[0]
    img = niend(img, sigma, pct)
    PBD().save(out_path, img.reshape(1, *img.shape))


if __name__ == '__main__':
    s_tab = pd.read_csv(wkdir / 'param.csv', index_col=0)
    out_dir.mkdir(exist_ok=True)
    arglist = []
    for f in crop_path.rglob('*.v3dpbd'):
        brain = int(f.name.split('_')[0])
        arglist.append((f, s_tab.at[brain, 'sigma'], s_tab.at[brain, 'pct']))

    # main((crop_path / "17545_21113_13119_3782.v3dpbd", 12, 1))

    with Pool(14) as p:
        for res in tqdm(p.imap(main, arglist), total=len(arglist)): pass
