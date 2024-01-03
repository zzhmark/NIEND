from v3dpy.loaders import PBD, Raw
from tifffile import imwrite
from pathlib import Path


def main(inpath):
    d = inpath.parent.name
    outpath = Path(r'D:\rectify\compressed') / d / inpath.with_suffix('.tiff').name
    outpath.parent.mkdir(exist_ok=True, parents=True)
    i = PBD().load(inpath)[0]
    imwrite(
        outpath,
        i,
        bigtiff=True,
        photometric='minisblack',
        planarconfig='separate',
        compression='lzma',
    )


if __name__ == "__main__":
    from tqdm import tqdm
    from multiprocessing import Pool

    imgdirs = [
        r"D:\rectify\crop_8bit",
        r"D:\rectify\my"
    ]
    for i in imgdirs:
        files = [*Path(i).glob('*.v3dpbd')]
        with Pool(14) as p:
            for j in tqdm(p.imap(main, files), total=len(files)): pass
