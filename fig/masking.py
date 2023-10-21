from pathlib import Path
from v3dpy.loaders import PBD
from tempfile import TemporaryDirectory
import os
from utils import swc_handler
wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'highpass_fig'
mandir = wkdir / 'manual'


def main(path):
    tree = swc_handler.parse_swc(mandir / path)
    tree = [t[:5] + (5,) + t[6:] for t in tree]
    path = Path(path).with_suffix('.v3dpbd')
    raw = PBD().load(crop_path / path.name)[0]
    high = PBD().load(out_dir / path)[0]

    raw = raw / (raw.max() - raw.min())
    high = high / (high.max() - high.min())
    with TemporaryDirectory() as td:
        td = Path(td)
        swc = td / 'tree.swc'
        swc_handler.write_swc(tree, td / 'tree.swc')
        mask = td / 'mask.v3dpbd'
        os.system(
            f'vaa3D-x /x maskimage_cylinder /f swc2mask /i {swc} /o {mask} /p {raw.shape[-1]} {raw.shape[-2]} {raw.shape[-3]} > NUL')
        mask = PBD().load(mask)[0]
        raw = raw[mask > 0]
        high = high[mask > 0]
    return path.stem, raw, high


if __name__ == '__main__':
    import pandas as pd
    from multiprocessing import Pool
    from tqdm import tqdm

    imgs = [i.with_suffix('.swc').name for i in out_dir.rglob('*.v3dpbd')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    imgs = [*filter(lambda f: tab.at[f, 'sparse'] == 1, imgs)]
    res = []
    with Pool(12) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)):
            res.append(i)

    import pickle
    with open(wkdir / 'masking.pickle', 'wb') as f:
        pickle.dump(res, f)
