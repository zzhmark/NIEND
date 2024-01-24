from pathlib import Path
from multiprocessing import Pool

import numpy as np
from v3dpy.loaders import PBD
from tqdm import tqdm
import tempfile
import subprocess


def raw_enh(in_path):
    out_path = out_dir / in_path.name
    if out_path.exists():
        return
    img = PBD().load(in_path)
    with tempfile.TemporaryDirectory() as tdir:
        temp = Path(tdir) / 'tmp.v3dpbd'
        PBD(pbd16_full_blood=False).save(temp, img)
        subprocess.run(['xvfb-run', '-a', 'Vaa3D-x', '-x', 'ada_threshold', '-f', 'adath', '-i', f'{temp}', '-o', f'{out_path}'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def raw_enh8(in_path):
    out_path = out_dir / in_path.name
    if out_path.exists():
        return
    img = PBD().load(in_path)
    img = (img * (255 / img.max())).astype('uint8')
    with tempfile.TemporaryDirectory() as tdir:
        temp = Path(tdir) / 'tmp.v3dpbd'
        PBD(pbd16_full_blood=False).save(temp, img)
        subprocess.run(['xvfb-run', '-a', 'Vaa3D-x', '-x', 'ada_threshold', '-f', 'adath', '-i', f'{temp}', '-o', f'{out_path}'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    files = [*Path("/PBshare/SEU-ALLEN/Users/zuohan/trans/crop1891/1st").glob('*.v3dpbd')]
    out_dir = Path('/PBshare/SEU-ALLEN/Users/zuohan/trans/rectify_1891/adathr8')
    out_dir.mkdir(exist_ok=True)
    
    with Pool(40) as p:
        # for res in tqdm(p.imap_unordered(raw_enh, files), total=len(files)): pass
        for res in tqdm(p.imap_unordered(raw_enh8, files), total=len(files)): pass

