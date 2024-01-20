# my new method
import os
from pathlib import Path
from niend import standard_niend
from v3dpy.loaders import PBD, Raw
import subprocess
from utils import swc_handler
import tempfile
import numpy as np


wkdir = Path(r"D:\rectify")
in_dir = wkdir / 'gold166'


def niend(in_path: Path):
    out_path = wkdir / 'bigneuron_niend' / in_path.relative_to(in_dir)
    if out_path.exists():
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    p = PBD()
    img = p.load(in_path)[0]
    swc = next(in_path.parent.glob('*.swc'))
    soma = [t for t in swc_handler.parse_swc(swc) if t[6] == -1][0][4:1:-1]
    soma = np.array(soma) / img.shape
    img = standard_niend(img, wavelet_levels=1, pct=2, soma=soma)
    PBD().save(out_path, img.reshape(1, *img.shape))


def guo(in_path: Path):
    out_path = wkdir / 'bigneuron_guo' / in_path.relative_to(in_dir)
    if out_path.exists():
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.system(f'Vaa3D-x /x imPreProcess /f im_enhancement /i {in_path} /o {out_path} > NUL 2> NUL')
    except:
        pass


def adath(in_path: Path):
    out_path = wkdir / 'bigneuron_adathr' / in_path.relative_to(in_dir)
    if out_path.exists():
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(f'Vaa3D-x /x ada_threshold /f adath /i {in_path} /o {out_path}',
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
    except:
        pass


def multiscale(in_path):
    out_path = wkdir / 'bigneuron_multi' / in_path.relative_to(in_dir)
    if out_path.exists():
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory() as tdir:
            tdir = Path(tdir)
            temp = tdir / 'temp.v3draw'
            img = PBD(pbd16_full_blood=False).load(in_path)
            Raw().save(temp, img)
            subprocess.run(f'Vaa3D-x /x multiscale /f adaptive_auto /i {temp} /o {temp}',
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            img = Raw().load(temp)
            PBD().save(out_path, img)
    except:
        pass


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm
    files = sorted(in_dir.rglob('*.v3dpbd'))
    with Pool(12) as p:
        for res in tqdm(p.imap(niend, files), total=len(files)): pass
        # for res in tqdm(p.imap(guo, files), total=len(files)): pass
        # for res in tqdm(p.imap(adath, files), total=len(files)): pass
        # for res in tqdm(p.imap(multiscale, files), total=len(files)): pass

