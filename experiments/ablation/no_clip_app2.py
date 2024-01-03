# this app2 script contains raw and new enhancement method
# run on windows

from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
import subprocess
import tempfile
import shutil
from v3dpy.loaders import PBD


wkdir = Path(r"D:\rectify")
rawdir = Path(r'Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st')


def main(name):
    in_file = wkdir / 'ablation' / 'clip' / name
    out_file = (wkdir / 'ablation' / 'clip_app2' / name).with_suffix('.swc')
    marker = wkdir / 'manual_marker' / (name + '.marker')
    if not marker.exists():
        marker = wkdir / "1024.marker"
        if out_file.exists():
            return
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tdir:
        t1 = Path(tdir) / 'temp.v3dpbd'
        t2 = Path(tdir) / 'temp.swc'
        shutil.copy(in_file, t1)
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {t1} /o {t2} /p {marker} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t2, out_file)
        except:
            print(f'{in_file} timeout.')


if __name__ == '__main__':
    files = [i.name for i in rawdir.glob('*.v3dpbd')]
    with Pool(12) as p:
        for res in tqdm(p.imap_unordered(main, files), total=len(files)): pass
