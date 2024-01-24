# this script is run on ubuntu 

import os
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
import subprocess
import tempfile
import shutil


def guo8(name):
    in_file = wkdir / 'guo_enh_8' / name
    out_file = (wkdir / 'guo8_app2' / name).with_suffix('.swc')
    out_file.parent.mkdir(exist_ok=True)
    marker = Path(f'manual_marker/{name}.marker')
    if not marker.exists():
        marker = "1024.marker"
    if out_file.exists():
        with open(out_file) as f:
            a = f.readlines()
            if len(a) > 25:
                return
            else:
                marker = 'NONE'
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        ret = subprocess.run(['timeout', '600s', 'xvfb-run', '-a', 'Vaa3D-x', '-x', 'vn2_no_ini', '-f', 'app2', '-i', 
                                in_file, '-o', t, '-p', marker, '0', 'AUTO', '0'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret.returncode == 124 or not t.exists():
            print(f'{in_file.name} failed')
        else:
            shutil.move(t, out_file)


def guo(name):
    in_file = wkdir / 'guo_enh' / name
    out_file = (wkdir / 'guo_app2' / name).with_suffix('.swc')
    out_file.parent.mkdir(exist_ok=True)
    marker = Path(f'manual_marker/{name}.marker')
    if not marker.exists():
        marker = "1024.marker"
    if out_file.exists():
        with open(out_file) as f:
            a = f.readlines()
            if len(a) > 25:
                return
            else:
                marker = 'NONE'
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        ret = subprocess.run(['timeout', '600s', 'xvfb-run', '-a', 'Vaa3D-x', '-x', 'vn2_no_ini', '-f', 'app2', '-i', 
                                in_file, '-o', t, '-p', marker, '0', 'AUTO', '0'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret.returncode == 124 or not t.exists():
            print(f'{in_file.name} failed')
        else:
            shutil.move(t, out_file)


def multiscale(name):
    in_file = (wkdir / 'multiscale' / name).with_suffix('.v3draw')
    out_file = (wkdir / 'multiscale_app2' / name).with_suffix('.swc')
    out_file.parent.mkdir(exist_ok=True)
    marker = Path(f'manual_marker/{name}.marker')
    if not marker.exists():
        marker = "1024.marker"
        # if out_file.exists():
        #     return
    if out_file.exists():
        with open(out_file) as f:
            a = f.readlines()
            if len(a) > 25:
                return
            else:
                marker = 'NONE'
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        ret = subprocess.run(['timeout', '600s', 'xvfb-run', '-a', 'Vaa3D-x', '-x', 'vn2_no_ini', '-f', 'app2', '-i', 
                                in_file, '-o', t, '-p', marker, '0', 'AUTO', '0'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret.returncode == 124 or not t.exists():
            print(f'{in_file.name} failed')
        else:
            os.system(f'mv {t} {out_file}')
            # shutil.move(t, out_file)


def adathr(name):
    in_file = (wkdir / 'adathr' / name)
    out_file = (wkdir / 'adathr_app2' / name).with_suffix('.swc')
    out_file.parent.mkdir(exist_ok=True)
    marker = Path(f'manual_marker/{name}.marker')
    if not marker.exists():
        marker = "1024.marker"
        # if out_file.exists():
        #     return
    if out_file.exists():
        with open(out_file) as f:
            a = f.readlines()
            if len(a) > 25:
                return
            else:
                marker = 'NONE'
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        ret = subprocess.run(['timeout', '600s', 'xvfb-run', '-a', 'Vaa3D-x', '-x', 'vn2_no_ini', '-f', 'app2', '-i', 
                                in_file, '-o', t, '-p', marker, '0', 'AUTO', '0'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret.returncode == 124 or not t.exists():
            print(f'{in_file.name} failed')
        else:
            os.system(f'mv {t} {out_file}')
            # shutil.move(t, out_file)


def adathr8(name):
    in_file = (wkdir / 'adathr8' / name)
    out_file = (wkdir / 'adathr8_app2' / name).with_suffix('.swc')
    out_file.parent.mkdir(exist_ok=True)
    marker = Path(f'manual_marker/{name}.marker')
    if not marker.exists():
        marker = "1024.marker"
        # if out_file.exists():
        #     return
    if out_file.exists():
        with open(out_file) as f:
            a = f.readlines()
            if len(a) > 25:
                return
            else:
                marker = 'NONE'
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        ret = subprocess.run(['timeout', '600s', 'xvfb-run', '-a', 'Vaa3D-x', '-x', 'vn2_no_ini', '-f', 'app2', '-i', 
                                in_file, '-o', t, '-p', marker, '0', 'AUTO', '0'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret.returncode == 124 or not t.exists():
            print(f'{in_file.name} failed')
        else:
            os.system(f'mv {t} {out_file}')
            # shutil.move(t, out_file)



def guo16(name):
    in_file = wkdir / 'guo_enh' / name
    out_file = (wkdir / 'guo_app2' / name).with_suffix('.swc')
    out_file.parent.mkdir(exist_ok=True)
    marker = Path(f'manual_marker/{name}.marker')
    if not marker.exists():
        marker = "1024.marker"
    if out_file.exists():
        with open(out_file) as f:
            a = f.readlines()
            if len(a) > 25:
                return
            else:
                marker = 'NONE'
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        ret = subprocess.run(['timeout', '600s', 'xvfb-run', '-a', 'Vaa3D-x', '-x', 'vn2_no_ini', '-f', 'app2', '-i', 
                                in_file, '-o', t, '-p', marker, '0', 'AUTO', '0'],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if ret.returncode == 124 or not t.exists():
            print(f'{in_file.name} failed')
        else:
            shutil.move(t, out_file)


if __name__ == '__main__':
    wkdir = Path("/PBshare/SEU-ALLEN/Users/zuohan/trans/rectify_1891")
    files = [i.name for i in (wkdir / '../crop1891/1st').glob('*.v3dpbd')]
    
    with Pool(25) as p:
        # for res in tqdm(p.imap_unordered(guo, files), total=len(files)): pass
        # for res in tqdm(p.imap_unordered(multiscale, files), total=len(files)): pass
        for res in tqdm(p.imap_unordered(adathr8, files), total=len(files)): pass
        # for res in tqdm(p.imap_unordered(guo8, files), total=len(files)): pass
        
        