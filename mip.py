from multiprocessing import Pool
from pathlib import Path
import matplotlib.pyplot as plt
from v3dpy.loaders import PBD
from tqdm import tqdm
import swc_handler
import numpy as np
import pandas as pd


wkdir = Path(r"D:\rectify")


def main(name):
    p1 = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st") / name
    p2 = wkdir / 'my_8bit' / name
    p = PBD()
    plt.figure()
    plt.subplot(2, 2, 1)
    img1 = p.load(p1)[0].max(axis=0)
    try:
        tree = swc_handler.parse_swc((wkdir / 'raw_app2' / name).with_suffix('.swc'))
        tree = np.transpose([i[2:4] for i in tree])
        plt.scatter(tree[0], tree[1], s=.1, c=['#ff0000'])
    except:
        pass
    plt.imshow(img1)
    plt.xticks([])
    plt.yticks([])
    plt.title('raw')

    plt.subplot(2, 2, 2)
    img2 = p.load(p2)[0].max(axis=0)
    plt.imshow(img2)
    plt.xticks([])
    plt.yticks([])
    plt.title('proc')

    plt.subplot(2, 2, 3)
    tree = swc_handler.parse_swc((wkdir / 'manual' / name).with_suffix('.swc'))
    tree = np.transpose([i[2:4] for i in tree])
    plt.scatter(tree[0], tree[1], s=.1, c=['#ff0000'])
    plt.imshow(img1)
    plt.xticks([])
    plt.yticks([])
    plt.title('gt')

    plt.subplot(2, 2, 4)
    tree = swc_handler.parse_swc((wkdir / 'my_app2' / name).with_suffix('.swc'))
    tree = np.transpose([i[2:4] for i in tree])
    plt.scatter(tree[0], tree[1], s=.1, c=['#ff0000'])
    plt.imshow(img2)
    plt.xticks([])
    plt.yticks([])
    plt.title('proc_recon')

    plt.savefig((wkdir / 'mip' / name).with_suffix('.png'), bbox_inches='tight', dpi=200)
    plt.close()


if __name__ == '__main__':
    (wkdir / 'mip').mkdir(exist_ok=True)
    raw = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
    df = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    files = [Path(i).with_suffix('.v3dpbd').name for i in df[df['sparse'] == 1].index]
    with Pool(12) as p:
        for res in tqdm(p.imap(main, files), total=len(files)):
            pass
