from pathlib import Path
from v3dpy.loaders import PBD
from tempfile import TemporaryDirectory
import os
from utils import swc_handler

serv_dir = Path(r'Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891')
wkdir = Path(r"D:\rectify")
raw_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
psf_dir = serv_dir / 'psf_post'
mandir = wkdir / 'manual_profile'
my_dir = wkdir / 'my'
scale = 2


def main(path: str):
    try:
        swc = mandir / path
        path = Path(path).with_suffix('.v3dpbd')
        img = PBD().load(raw_path / path)[0]
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

        raw1 = img[mask > 0]
        raw2 = img[mask2 > mask]
        raw_stat = img.mean(), img.std()

        img = PBD().load(psf_dir / path.name)[0]
        psf1 = img[mask > 0]
        psf2 = img[mask2 > mask]
        psf_stat = img.mean(), img.std()

        img = PBD().load(my_dir / path)[0]
        my1 = img[mask > 0]
        my2 = img[mask2 > mask]
        my_stat = img.mean(), img.std()

    except Exception as e:
        print(e)
        return None

    return {
        'name': path,
        'raw': (raw1, raw2, raw_stat),
        'my': (my1, my2, my_stat),
        'psf': (psf1, psf2, psf_stat),
        }


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm
    import pandas as pd

    imgs = [i.with_suffix('.swc').name for i in psf_dir.rglob('*.v3dpbd')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    imgs = [*filter(lambda f: tab.at[f, 'sparse'] == 1, imgs)]
    res = []
    with Pool(14) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)):
            if i is not None:
                res.append(i)

    import pickle
    with open(wkdir / 'psf_masking_final.pickle', 'wb') as f:
        pickle.dump(res, f)
