from v3dpy.loaders import PBD
indir = r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st"
outdir = r"D:\rectify\crop_8bit"


def main(path):
    i = PBD().load(path)
    i = (i * (255 / i.max())).astype('uint8')
    PBD().save(outdir / path.relative_to(indir), i)


if __name__ == '__main__':
    from multiprocessing import Pool
    from pathlib import Path
    from tqdm import tqdm

    imgs = [*Path(indir).glob('*.v3dpbd')]
    Path(outdir).mkdir(exist_ok=True)

    with Pool(14) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)):
            pass