# my new method

from pathlib import Path
from multiprocessing import Pool

import pandas as pd
from v3dpy.loaders import PBD
from niend import standard_niend
from tqdm import tqdm

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'my'


def main(args):
    in_path, sigma, pct = args
    out_path = out_dir / in_path.name
    if out_path.exists():
        return
    img = PBD().load(in_path)[0]
    img = standard_niend(img, sigma, pct)
    PBD().save(out_path, img.reshape(1, *img.shape))


if __name__ == '__main__':
    s_tab = pd.read_csv(wkdir / 'param.csv', index_col=0)
    out_dir.mkdir(exist_ok=True)
    arglist = []
    for f in crop_path.rglob('*.v3dpbd'):
        brain = int(f.name.split('_')[0])
        arglist.append((f, s_tab.at[brain, 'sigma'], s_tab.at[brain, 'pct']))

    # main((r"C:\Users\zzh\Downloads\0011.tiff", 12, 1))

    with Pool(12) as p:
        for res in tqdm(p.imap(main, arglist), total=len(arglist)): pass

