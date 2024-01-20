# this app2 script contains raw and new enhancement method
# run on windows

from pathlib import Path
import subprocess
import tempfile
import shutil
from utils import swc_handler


wkdir = Path(r"D:\rectify")
rawdir = wkdir / 'gold166'
mydir = wkdir / 'bigneuron_niend'
guodir = wkdir / 'bigneuron_guo'
adadir = wkdir / 'bigneuron_adathr'
multidir = wkdir / 'bigneuron_multi'


def raw(in_file: Path):
    in_file = rawdir / in_file.relative_to(mydir)
    out_file = (wkdir / 'bigneuron_app2' / in_file.relative_to(rawdir)).with_suffix('.swc')
    if out_file.exists():
        return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        t1 = tdir / 'temp.v3dpbd'
        t2 = tdir / 'temp.swc'
        treefile = next(in_file.parent.glob('*.swc'))
        tree = swc_handler.parse_swc(treefile)
        x, y, z = [t for t in tree if t[6] == -1][0][2:5]
        marker = tdir / 'temp.marker'
        with open(marker, 'w') as f:
            f.write('#x, y, z, radius, shape, name, comment,color_r,color_g,color_b'
                    f'{x}, {y}, {z}, 5.000000, 1, , , 207, 52, 139')
        shutil.copy(in_file, t1)
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {t1} /o {t2} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t2, out_file)
        except:
            print(f'{in_file} timeout.')


def my(in_file: Path):
    out_file = (wkdir / 'bigneuron_niend_app2' / in_file.relative_to(mydir)).with_suffix('.swc')
    if out_file.exists():
        return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        t1 = tdir / 'temp.v3dpbd'
        t2 = tdir / 'temp.swc'
        treefile = next((rawdir / in_file.relative_to(mydir).parent).glob('*.swc'))
        tree = swc_handler.parse_swc(treefile)
        x, y, z = [t for t in tree if t[6] == -1][0][2:5]
        marker = tdir / 'temp.marker'
        with open(marker, 'w') as f:
            f.write('#x, y, z, radius, shape, name, comment,color_r,color_g,color_b'
                    f'{x}, {y}, {z}, 5.000000, 1, , , 207, 52, 139')
        shutil.copy(in_file, t1)
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {t1} /o {t2} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t2, out_file)
        except:
            print(f'{in_file} timeout.')


def guo(in_file: Path):
    out_file = (wkdir / 'bigneuron_guo_app2' / in_file.relative_to(mydir)).with_suffix('.swc')
    treefile = next((rawdir / in_file.relative_to(mydir).parent).glob('*.swc'))
    in_file = guodir / in_file.relative_to(mydir)
    if out_file.exists() or not in_file.exists():
        return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        t1 = tdir / 'temp.v3dpbd'
        t2 = tdir / 'temp.swc'
        tree = swc_handler.parse_swc(treefile)
        x, y, z = [t for t in tree if t[6] == -1][0][2:5]
        marker = tdir / 'temp.marker'
        with open(marker, 'w') as f:
            f.write('#x, y, z, radius, shape, name, comment,color_r,color_g,color_b'
                    f'{x}, {y}, {z}, 5.000000, 1, , , 207, 52, 139')
        shutil.copy(in_file, t1)
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {t1} /o {t2} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t2, out_file)
        except:
            print(f'{in_file} timeout.')


def multiscale(in_file: Path):
    out_file = (wkdir / 'bigneuron_multi_app2' / in_file.relative_to(mydir)).with_suffix('.swc')
    treefile = next((rawdir / in_file.relative_to(mydir).parent).glob('*.swc'))
    in_file = multidir / in_file.relative_to(mydir)
    if out_file.exists() or not in_file.exists():
        return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        t1 = tdir / 'temp.v3dpbd'
        t2 = tdir / 'temp.swc'
        tree = swc_handler.parse_swc(treefile)
        x, y, z = [t for t in tree if t[6] == -1][0][2:5]
        marker = tdir / 'temp.marker'
        with open(marker, 'w') as f:
            f.write('#x, y, z, radius, shape, name, comment,color_r,color_g,color_b'
                    f'{x}, {y}, {z}, 5.000000, 1, , , 207, 52, 139')
        shutil.copy(in_file, t1)
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {t1} /o {t2} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t2, out_file)
        except:
            print(f'{in_file} timeout.')


def adathr(in_file: Path):
    out_file = (wkdir / 'bigneuron_adathr_app2' / in_file.relative_to(mydir)).with_suffix('.swc')
    treefile = next((rawdir / in_file.relative_to(mydir).parent).glob('*.swc'))
    in_file = adadir / in_file.relative_to(mydir)
    if out_file.exists() or not in_file.exists():
        return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        tdir = Path(tdir)
        t1 = tdir / 'temp.v3dpbd'
        t2 = tdir / 'temp.swc'
        tree = swc_handler.parse_swc(treefile)
        x, y, z = [t for t in tree if t[6] == -1][0][2:5]
        marker = tdir / 'temp.marker'
        with open(marker, 'w') as f:
            f.write('#x, y, z, radius, shape, name, comment,color_r,color_g,color_b'
                    f'{x}, {y}, {z}, 5.000000, 1, , , 207, 52, 139')
        shutil.copy(in_file, t1)
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {t1} /o {t2} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t2, out_file)
        except:
            print(f'{in_file} timeout.')


if __name__ == '__main__':
    from tqdm import tqdm
    from multiprocessing import Pool
    files = sorted(mydir.rglob('*.v3dpbd'))
    with Pool(12) as p:
        for res in tqdm(p.imap_unordered(my, files), total=len(files)): pass
        # for res in tqdm(p.imap_unordered(raw, files), total=len(files)): pass
        # for res in tqdm(p.imap_unordered(guo, files), total=len(files)): pass
        # for res in tqdm(p.imap_unordered(multiscale, files), total=len(files)): pass
        # for res in tqdm(p.imap_unordered(adathr, files), total=len(files)): pass
