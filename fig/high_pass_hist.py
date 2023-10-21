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
    import pickle


    ppath = wkdir / 'hist_high.pickle'
    if ppath.exists():
        with open(ppath, 'rb') as f:
            res = pickle.load(f)
    else:
        imgs = [i.with_suffix('.swc').name for i in out_dir.rglob('*.v3dpbd')]
        tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
        imgs = [*filter(lambda f: tab.at[f, 'sparse'] == 1, imgs)]
        res = []
        with Pool(12) as p:
            for r,h in tqdm(p.imap(main, imgs), total=len(imgs)):
                res.append((r, h))
        with open(ppath, 'wb') as f:
            pickle.dump(res, f)

    import matplotlib.pyplot as plt
    rr = [r[0] for r, h in res]
    hh = [h[0] for r, h in res]
    print(rr[0])
    rr = np.mean(rr, axis=0)
    hh = np.mean(hh, axis=0)
    plt.plot(np.linspace(0, 1, 40), rr)
    plt.plot(np.linspace(0, 1, 40), hh)
    # plt.yscale('log')
    plt.ylim(0, 2e4)
    plt.show()
