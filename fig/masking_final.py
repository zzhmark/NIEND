from pathlib import Path
from v3dpy.loaders import PBD, Raw
from tempfile import TemporaryDirectory
import os
from utils import swc_handler

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
ada_dir = Path(r'Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\adathr')
multi_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\multiscale")
guo_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\guo_enh_8")
my_dir = wkdir / 'my'
mandir = wkdir / 'manual_profile'

scale = 2


def main(path):
    swc = mandir / path
    path = Path(path).with_suffix('.v3dpbd')
    img = PBD().load(crop_path / path)[0]
    raw = img
    with TemporaryDirectory() as td:
        td = Path(td)
        tree = swc_handler.parse_swc(swc)
        tree = [t[:5] + (scale*t[5],) + t[6:] for t in tree]
        swc2 = td / 'tree.swc'
        swc_handler.write_swc(tree, swc2)
        mask = td / 'mask.v3dpbd'
        mask2 = td / 'mask2.v3dpbd'
        os.system(
            f'vaa3D-x /x maskimage_cylinder /f swc2mask /i {swc} /o {mask} /p {raw.shape[-1]} {raw.shape[-2]} {raw.shape[-3]} > NUL 2> NUL')
        os.system(
            f'vaa3D-x /x maskimage_cylinder /f swc2mask /i {swc2} /o {mask2} /p {raw.shape[-1]} {raw.shape[-2]} {raw.shape[-3]} > NUL 2> NUL')
        mask = PBD().load(mask)[0]
        mask2 = PBD().load(mask2)[0]

    try:
        raw1 = img[mask > 0]
        raw2 = img[mask2 > mask]

        img = PBD().load(my_dir / path)[0]
        my1 = img[mask > 0]
        my2 = img[mask2 > mask]

        img = Raw().load(multi_dir / path.with_suffix('.v3draw'))[0]
        multi1 = img[mask > 0]
        multi2 = img[mask2 > mask]

        img = PBD().load(ada_dir / path)[0]
        ada1 = img[mask > 0]
        ada2 = img[mask2 > mask]

        img = PBD().load(guo_dir / path)[0]
        guo1 = img[mask > 0]
        guo2 = img[mask2 > mask]
    except Exception as e:
        print(e)
        return None

    return {'raw': (raw1, raw2),
            'my': (my1, my2),
            'guo': (guo1, guo2),
            'multi': (multi1, multi2),
            'ada': (ada1, ada2)
            }


if __name__ == '__main__':
    import pandas as pd
    from multiprocessing import Pool
    from tqdm import tqdm

    imgs = [i.with_suffix('.swc').name for i in my_dir.rglob('*.v3dpbd')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    imgs = [*filter(lambda f: tab.at[f, 'sparse'] == 1, imgs)]
    res = []
    with Pool(16) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)):
            if i is not None:
                res.append(i)

    import pickle
    with open(wkdir / 'masking_final.pickle', 'wb') as f:
        pickle.dump(res, f)
