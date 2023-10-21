from pathlib import Path
from skimage import io
from v3dpy.loaders import PBD
from multiprocessing import Pool
from tqdm import tqdm
import numpy as np

wkdir = Path(r'D:\rectify')

out_dir = wkdir / 'human_crop'
out_dir.mkdir(exist_ok=True)

def main(img_folder):
    outpath = out_dir / (img_folder.name + '.v3dpbd')
    print(img_folder)
    img = io.imread_collection(str(img_folder / '*.tif'), plugin='simpleitk')
    img = np.array([np.flip(img.concatenate(), axis=1)])
    PBD(pbd16_full_blood=False).save(outpath, img)



if __name__ == '__main__':
    dir1 = wkdir / r'human\20230706'
    dir2 = wkdir / r'human\20230704'
    img1 = [*dir1.glob('Z*')]
    img2 = [*dir2.glob('Z*')]
    with Pool(12) as p:
        for res in tqdm(p.imap(main, img1), total=len(img1)): pass
        for res in tqdm(p.imap(main, img2), total=len(img2)): pass

