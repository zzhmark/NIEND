from pathlib import Path

import numpy as np
from v3dpy.loaders import PBD
from utils import swc_handler
from random import sample

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'highpass_fig'
mandir = wkdir / 'manual'

sampling = 100
imgct = np.array([512, 512, 128])
rad = np.array([32, 32, 8])


def main(path):
    tree = swc_handler.parse_swc(mandir / path)
    tree = [*filter(lambda t: (np.abs(t[2:5] - imgct) < imgct - rad).all(), tree)]
    tree = sample(tree, sampling)
    path = Path(path).with_suffix('.v3dpbd')
    raw = PBD().load(crop_path / path.name)[0]
    high = PBD().load(out_dir / path)[0]
    res1 = []
    res2 = []
    raw = raw / (raw.max() - raw.min())
    high = high / (high.max() - high.min())
    for t in tree:
        xb, yb, zb = (t[2:5] - rad).astype(int)
        xe, ye, ze = (t[2:5] + rad).astype(int)
        r = raw[zb:ze, yb:ye, xb:xe]
        h = high[zb:ze, yb:ye, xb:xe]
        res1.append(r.mean() + .5 * r.std())
        res2.append(h.mean() + .5 * h.std())
    return res1, res2


if __name__ == '__main__':
    import pandas as pd
    from multiprocessing import Pool
    from tqdm import tqdm

    imgs = [i.with_suffix('.swc').name for i in out_dir.rglob('*.v3dpbd')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    imgs = [*filter(lambda f: tab.at[f, 'sparse'] == 1, imgs)]
    res = []
    with Pool(14) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)):
            res.append(i)

    import pickle
    with open(wkdir / 'thr_sampling.pickle', 'wb') as f:
        pickle.dump(res, f)
