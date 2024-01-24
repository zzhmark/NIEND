from pathlib import Path
from multiprocessing import Pool

import numpy as np
from v3dpy.loaders import PBD
from v3dpy.loaders import Raw
from tqdm import tqdm
import tempfile
import subprocess


def raw_enh(in_path):
    out_path = out_dir / in_path.with_suffix('.v3draw').name
    if out_path.exists():
        return
    img = PBD().load(in_path)
    img = (img / img.max() * 255).astype('uint8')
    with tempfile.TemporaryDirectory() as tdir:
        temp = Path(tdir) / 'tmp.v3draw'
        Raw().save(temp, img)
        subprocess.run(['xvfb-run', '-a', 'Vaa3D-x', '-x', 'multiscale', '-f', 'adaptive_auto', '-i', f'{temp}', '-o', f'{out_path}', 
                        '-p', '2', '1', '0.5', '1', '1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == '__main__':
    files = [*Path("/PBshare/SEU-ALLEN/Users/zuohan/trans/crop1891/1st").glob('*.v3dpbd')]
    out_dir = Path('/home/zzh/PBshare/SEU-ALLEN/Users/zuohan/trans/rectify_1891/multiscale')
    out_dir.mkdir(exist_ok=True)
    
    with Pool(15) as p:
        for res in tqdm(p.imap_unordered(raw_enh, files), total=len(files)): pass

