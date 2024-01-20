from skimage.restoration import richardson_lucy
from v3dpy.loaders import PBD
from pathlib import Path
import numpy as np


wkdir = Path(r"D:\rectify")
in_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'psf'


def l_r(path: Path):
    img = PBD().load(path)[0]
    img = img / img.max()
    outpath = out_dir / path.name
    psf = np.ones((5, 5)) / 25
    for i in range(img.shape[0]):
        img[i] = 1 - richardson_lucy(img[i], psf, num_iter=30)
    m1, m2 = img.max(), img.min()
    out = ((img - m1) * (255 / (m2 - m1))).astype('uint8')
    PBD().save(outpath, np.array([out]))


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm
    out_dir.mkdir(exist_ok=True, parents=True)
    files = sorted(in_dir.rglob('*.v3dpbd'))
    # l_r(files[0])
    with Pool(12) as p:
        for res in tqdm(p.imap(l_r, files), total=len(files)): pass