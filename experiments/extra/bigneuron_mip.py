# my new method
from pathlib import Path
from v3dpy.loaders import PBD, Raw
from utils.file_io import load_image
import tifffile


wkdir = Path(r"D:\rectify")
in_dir = wkdir / 'gold166'
out_dir = wkdir / 'bigneuron_mip'


def mip(path: Path):
    outpath = out_dir / path.with_suffix('.tiff').name
    i = PBD().load(path)[0] if path.suffix == '.v3dpbd' else Raw().load(path)[0]
    i = i.max(axis=0)
    tifffile.imwrite(outpath, i)


if __name__ == '__main__':
    out_dir.mkdir(exist_ok=True, parents=True)
    from multiprocessing import Pool
    from tqdm import tqdm
    files = sorted(in_dir.rglob('*.v3dpbd')) + sorted(in_dir.rglob('*.v3draw'))
    with Pool(12) as p:
        for res in tqdm(p.imap(mip, files), total=len(files)): pass

