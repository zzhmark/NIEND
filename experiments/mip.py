from v3dpy.loaders import PBD
import tifffile

out_dir = r"D:\book_cover\mip"
in_dir = r"D:\rectify\my"


def main(path):
    outpath = out_dir / path.relative_to(in_dir).with_suffix('.tiff')
    i = PBD().load(path)[0]
    i = i.max(axis=0)
    tifffile.imwrite(outpath, i)


if __name__ == '__main__':
    from pathlib import Path
    from tqdm import tqdm
    from multiprocessing import Pool

    imgs = [*Path(in_dir).glob('*.v3dpbd')]

    with Pool(14) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)):
            pass
