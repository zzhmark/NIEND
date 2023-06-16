from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
import subprocess
import tempfile
import shutil


wkdir = Path(r"D:\rectify")


def main(args):
    in_file, out_file = args
    if out_file.exists():
        return
    with tempfile.TemporaryDirectory() as tdir:
        t = Path(tdir) / 'temp.swc'
        try:
            subprocess.run(f'Vaa3D-x /x vn2 /f app2 /i {in_file} /o {t} /p {wkdir / "1024.marker"} 0 AUTO 0',
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
            shutil.move(t, out_file)
        except:
            print(f'{in_file} timeout.')


if __name__ == '__main__':
    in_dir = wkdir / 'guo_enh'
    out_dir = wkdir / 'guo_app2'
    in_file = [*in_dir.glob('*.v3dpbd')]
    out_dir.mkdir(exist_ok=True)
    out_file = [out_dir / i.relative_to(in_dir).with_suffix('.swc') for i in in_file]
    with Pool(12) as p:
        for res in tqdm(p.imap(main, zip(in_file, out_file)), total=len(in_file)):
            pass