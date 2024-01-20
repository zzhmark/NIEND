from pathlib import Path
import os

wkdir = Path(r"D:\rectify")
raw_path = wkdir / 'gold166'
out_dir = wkdir / 'bigneuron_profile'


def main(img_path: Path):
    swc_path = next((img_path.parent).glob('*.swc'))
    out_path = out_dir / img_path.relative_to(raw_path).with_suffix('.swc')
    out_path.parent.mkdir(exist_ok=True, parents=True)
    os.system(f'Vaa3D-x /x neuron_radius /f neuron_radius /i {img_path} {swc_path} /o {out_path} /p 30 1 > NUL 2> NUL')


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm

    imgs = sorted(raw_path.rglob('*.v3dpbd')) + sorted(raw_path.rglob('*v3draw'))
    with Pool(14) as p:
        for i in tqdm(p.imap(main, imgs), total=len(imgs)): pass

