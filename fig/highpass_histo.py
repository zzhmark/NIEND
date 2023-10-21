from pathlib import Path

import numpy as np
from skimage.exposure import histogram

from v3dpy.loaders import PBD

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'highpass_fig'


def main(path):
    path = Path(path).with_suffix('.v3dpbd')
    raw = PBD().load(crop_path / path.name)
    high = PBD().load(out_dir / path)
    r = np.histogram(raw, bins=40)
    h = np.histogram(high, bins=40)
    return r,h


if __name__ == '__main__':
    import pandas as pd
    from multiprocessing import Pool
    from tqdm import tqdm
    from random import sample

    imgs = [i.with_suffix('.swc').name for i in out_dir.rglob('*.v3dpbd')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    imgs = [*filter(lambda f: tab.at[f, 'sparse'] == 1, imgs)]
    nrow, ncol = 6, 4
    imgs = sample(imgs, nrow * ncol)
    res = []
    with Pool(12) as p:
        for r,h in tqdm(p.imap(main, imgs), total=len(imgs)):
            res.append((r, h))

    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(nrow, ncol, layout='constrained', figsize=(ncol*4, nrow*2))
    for ax, (r, h) in zip(axs.flat, res):
        ax.plot(h[1][:-1], h[0])
        ax.plot(r[1][:-1], r[0])
        ax.set_yscale('log')
        ax.set_ylim(1, None)
    plt.show()
