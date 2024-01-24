from v3dpy.loaders import PBD
from tifffile import imwrite
from pathlib import Path


def main(inpath: Path):
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

    main(Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st\15257_13263_25518_2294.v3dpbd"))