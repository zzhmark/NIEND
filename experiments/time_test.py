# my new method

from pathlib import Path
from multiprocessing import Pool

import pandas as pd
from v3dpy.loaders import PBD
from niend import standard_niend
from tqdm import tqdm
# from memory_profiler import profile
import time
from random import sample

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")


test_small = False


# @profile
def main(args):
    t1 = time.time()
    in_path, sigma, pct = args
    img = PBD().load(in_path)[0]
    if test_small:
        img = img[0,:, 384: 640, 384: 640]
    img = standard_niend(img, sigma, pct)
    t2 = time.time()
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

    tt = []
    arglist = sample(arglist, 30)
    with Pool(1) as p:
        for t in tqdm(p.imap(main, arglist), total=len(arglist)):
            tt.append(t)
    tt = tt[10:]
    import pickle
    with open(wkdir / ('time_use_256.pickle' if test_small else 'time_use.pickle'), 'wb') as f:
        pickle.dump(tt, f)

