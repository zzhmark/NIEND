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
        subprocess.run(['xvfb-run', '-a', 'Vaa3D-x', '-x', 'imPreProcess', '-f', 'im_enhancement', '-i', f'{temp}', '-o', f'{out_path}'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def raw_enh_8(in_path):
    out_path = out_dir2 / in_path.name
    if out_path.exists():
        return
    img = PBD().load(in_path)
    with tempfile.TemporaryDirectory() as tdir:
        temp = Path(tdir) / 'tmp.v3dpbd'
        img = (img * (255 / img.max())).astype('uint8')
        PBD(pbd16_full_blood=False).save(temp, img)
        subprocess.run(['xvfb-run', '-a', 'Vaa3D-x', '-x', 'imPreProcess', '-f', 'im_enhancement', '-i', f'{temp}', '-o', f'{out_path}'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def raw_enh_16(in_path):
    out_path = out_dir3 / in_path.name
    if out_path.exists():
        return
    img = PBD().load(in_path)
    with tempfile.TemporaryDirectory() as tdir:
        temp = Path(tdir) / 'tmp.v3dpbd'
        img = (img * (65535 / img.max())).astype('uint16')
        PBD(pbd16_full_blood=False).save(temp, img)
        subprocess.run(['xvfb-run', '-a', 'Vaa3D-x', '-x', 'imPreProcess', '-f', 'im_enhancement', '-i', f'{temp}', '-o', f'{out_path}', 
                        '-p', '3', '1', f'{65535 * 35 // 255}'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    files = [*Path("/PBshare/SEU-ALLEN/Users/zuohan/trans/crop1891/1st").glob('*.v3dpbd')]
    out_dir = Path('/PBshare/SEU-ALLEN/Users/zuohan/trans/rectify_1891/guo_enh')
    out_dir.mkdir(exist_ok=True)
    
    out_dir2 = Path('/PBshare/SEU-ALLEN/Users/zuohan/trans/rectify_1891/guo_enh_8')
    out_dir2.mkdir(exist_ok=True)
    
    out_dir3 = Path('/PBshare/SEU-ALLEN/Users/zuohan/trans/rectify_1891/guo_enh_16')
    out_dir3.mkdir(exist_ok=True)
    
    with Pool(20) as p:
        # for res in tqdm(p.imap_unordered(raw_enh_8, files), total=len(files)): pass
        for res in tqdm(p.imap_unordered(raw_enh_16, files), total=len(files)): pass

