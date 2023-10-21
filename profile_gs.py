"""
resolving human neuron radius
Zuohan ZHao, 0922
"""

from pathlib import Path
from multiprocessing import Pool
import os

from v3dpy.loaders import PBD
from tempfile import TemporaryDirectory

img_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\adathr8")
swc_dir = Path(r'D:\rectify\manual')
# filenames may differ, but the IDs are matched
out_dir = Path(r'D:\rectify\manual_profile')


def main(img_path: Path):
    swc_path = swc_dir / img_path.with_suffix('.swc').name
    out_path = out_dir / swc_path.name
    os.system(f'Vaa3D-x.exe /x neuron_radius /f neuron_radius /i "{img_path}" "{swc_path}" '
              f'/p 5 1 /o {out_path} > NUL 2> NUL')


if __name__ == '__main__':
    imgs = [*Path(img_dir).glob('*.v3dpbd')]
    out_dir.mkdir(exist_ok=True)
    from tqdm import tqdm
    with Pool(14) as p:
        for res in tqdm(p.imap(main, imgs), total=len(imgs)): pass