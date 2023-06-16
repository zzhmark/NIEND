from pathlib import Path
from multiprocessing import Pool

import numpy as np
from v3dpy.loaders import PBD
from tqdm import tqdm
import tempfile
import subprocess


def main(args):
    in_path, out_path = args
    if out_path.exists():
        return
    p = PBD()
    img = p.load(in_path)
    mi = img.min()
    img = ((img - mi) * (255 / (img.max() - mi))).astype(np.uint8)
    with tempfile.TemporaryDirectory() as tdir:
        temp = Path(tdir) / 'tmp.v3dpbd'
        p.save(temp, img)
        subprocess.run(f'Vaa3D-x /x neuron_image_denoise /f guo_enh /i {temp} /o {out_path} /p enh_sigma 1,1,0.3',
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
    wkdir = Path(r"D:\rectify")
    out_dir = wkdir / 'guo_8bit'
    out_dir.mkdir(exist_ok=True)

    arglist = []
    for f in crop_path.glob('*.v3dpbd'):
        arglist.append((f, out_dir / f.name))
    with Pool(12) as p:
        for res in tqdm(p.imap(main, arglist), total=len(arglist)):
            pass

