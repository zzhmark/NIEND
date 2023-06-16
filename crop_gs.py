import os
import swc_handler
from tqdm import tqdm
import numpy as np
from pathlib import Path
from multiprocessing import Pool

new_dir = Path('D:/rectify/manual')


def main(args):
    in_path = args
    crop_box = [256, 1024, 1024]
    shift = [512, 512, 128]
    tree = swc_handler.parse_swc(in_path)
    soma = np.array([t[2:5] for t in tree if t[6] == -1][0], dtype=int)
    br = in_path.stem.split('_')
    if br[0].startswith('p'):
        br = br[1]
    else:
        br = br[0]
    if br == '210254':
        br = '15257'
    out_path = new_dir / f'{br}_{soma[0]}_{soma[1]}_{soma[2]}.swc'
    tree = [(*t[:2], *list(t[2:5] - soma + shift), 1, *t[6:]) for t in tree]
    tree = swc_handler.trim_swc(tree, crop_box)
    swc_handler.write_swc(tree, out_path)


if __name__ == '__main__':
    gs_dir = Path(r'Z:\SEU-ALLEN\Projects\fullNeurons\V2023_01_10\manual_final\All1891')
    new_dir.mkdir(exist_ok=True)
    arglist = [*gs_dir.glob("*.swc")]
    with Pool(12) as p:
        for swc in tqdm(p.imap(main, arglist, chunksize=20), total=len(arglist)):
            pass
