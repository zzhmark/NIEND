from pathlib import Path
import numpy as np
from v3dpy.loaders import PBD
from multiprocessing import Pool
from tqdm import tqdm
import pickle


def percentiles(path):
    img = PBD().load(path).flatten()
    counts = np.percentile(img, np.arange(0, 101))
    return counts


def count_pixels_percentiles(path):
    img = PBD().load(path).flatten()
    return np.histogram(img, 100)[0]


if __name__ == "__main__":

    wkdir = Path(r"D:\rectify")
    rawdir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
    raw_img = [*rawdir.glob('*.v3dpbd')]
    enh_img = [*(wkdir / 'my').glob('*.v3dpbd')]
    with Pool(20) as p:
        counts = []
        for c in tqdm(p.imap(count_pixels_percentiles, raw_img), total=len(raw_img)):
            counts.append(c)
        counts = np.vstack(counts)
        with open(wkdir / 'fig' / 'raw_hist.pickle', 'wb') as f:
            pickle.dump((counts, raw_img), f)

        counts = []
        for c in tqdm(p.imap(count_pixels_percentiles, enh_img), total=len(enh_img)):
            counts.append(c)
        counts = np.vstack(counts)
        with open(wkdir / 'fig' / 'enh_hist.pickle', 'wb') as f:
            pickle.dump((counts, enh_img), f)