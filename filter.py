from pathlib import Path
from multiprocessing import Pool

import pandas as pd
from v3dpy.loaders import PBD
from neuron_image_denoise.filter import *
from tqdm import tqdm

wkdir = Path(r"D:\rectify")


def main(args):
    in_path, out_path, sigma = args
    if out_path.exists():
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    p = PBD()
    img = p.load(in_path)[0]
    img = adaptive_sectional_feedforward_filter(img, sigma)
    # thr = 2 * (img.astype(int)[(img > 0) & (img < 256)] ** 2).mean() ** .5
    # img[img < thr] = 0
    # img = img.clip(None, 255).astype(np.uint8)
    # img = (img - img.min()) * (255 / (img.max() - img.min()))
    img = np.array([img])
    PBD().save(out_path, img)


def to8bit_clip(in_path):
    out_path = wkdir / 'my_8bit_clip' / in_path.name
    out_path.parent.mkdir(exist_ok=True)
    if out_path.exists():
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    p = PBD()
    img = p.load(in_path)
    thr = 2 * (img.astype(int)[(img > 0) & (img < 256)] ** 2).mean() ** .5
    img = img.clip(None, 255).astype(np.uint8)
    # img = ((img - img.min()) * (255 / (img.max() - img.min()))).astype('uint8')
    PBD().save(out_path, img)


if __name__ == '__main__':
    crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
    out_dir = wkdir / 'my_16bit'
    s_tab = pd.read_csv(wkdir / 'param.csv', index_col=0)

    arglist = []
    for f in crop_path.rglob('*.v3dpbd'):
        brain = int(f.name.split('_')[0])
        arglist.append((f, out_dir / f.relative_to(crop_path), s_tab.at[brain, 'sigma_new']))

    files = [a[1] for a in arglist]

    with Pool(12) as p:
        # for res in tqdm(p.imap(main, arglist), total=len(arglist)): pass
        for res in tqdm(p.imap(to8bit_clip, files), total=len(files)): pass

