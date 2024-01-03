from v3dpy.loaders import PBD, Raw

indir = r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\multiscale"
outdir = r"D:\rectify\multiscale_8bit"

def main(path):
    i = Raw().load(path)
    PBD().save(outdir / path.relative_to(indir).with_suffix('.v3dpbd'), i)


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm
    from pathlib import Path

    Path(outdir).mkdir(exist_ok=True)
    imgs = [*Path(indir).glob('*.v3draw')]

    with Pool(14) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)):
            pass