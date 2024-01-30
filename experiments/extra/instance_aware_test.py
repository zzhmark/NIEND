# computing 0.5 max soma intensity for 1891 neurons
# this is for validating that the instance-aware mechanism takes effect in rare cases

from pathlib import Path
from v3dpy.loaders import PBD
import numpy as np

wkdir = Path(r"D:\rectify")
in_path = wkdir / 'highpass_only'      # this folder contains images only processed with high-pass steps


def main(args):
    in_path, sigma, pct = args
    win = np.array((32, 128, 128))
    soma = (.5, .5, .5)
    img = PBD().load(in_path)[0]
    ct = (np.array(soma) * img.shape).astype(int)
    a = (ct - win // 2).clip(0)
    b = (ct + win // 2).clip(None, img.shape)
    thr = np.percentile(img, 100 - pct)
    stat = img[a[0]:b[0], a[1]:b[1], a[2]:b[2]].max() * .5
    return thr, stat


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm
    import pandas as pd
    s_tab = pd.read_csv(wkdir / 'param.csv', index_col=0)

    arglist = []
    for f in sorted(in_path.glob('*.v3dpbd')):
        brain = int(f.name.split('_')[0])
        arglist.append((f, s_tab.at[brain, 'sigma'], s_tab.at[brain, 'pct']))

    out = []
    with Pool(12) as p:
        for res in tqdm(p.imap(main, arglist), total=len(arglist)):
            out.append(res)

    import pickle
    with open(wkdir / 'instance_awareness.pickle', 'wb') as f:
        pickle.dump(out, f)


