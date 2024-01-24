# evaluate different reconstruction against gold standard

from utils.neuron_quality import DistanceEvaluation
import pandas as pd
from pathlib import Path
from multiprocessing import Pool
import sys
import os
import traceback
from tqdm import tqdm


wkdir = Path(r"D:\rectify")
serv_dir = Path(r'Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891')
psf_dir = serv_dir / 'psf_app2'
raw_dir = wkdir / 'raw_app2'


class HidePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def main(name: str):
    man = wkdir / 'manual' / name
    my = wkdir / 'my_app2' / name
    psf = psf_dir / name
    raw = raw_dir / name

    try:
        with HidePrint():
            de = DistanceEvaluation(15)
            my = de.run(my, man) if my.exists() else None
            psf = de.run(psf, man) if psf.exists() else None
            raw = de.run(raw, man) if raw.exists() else None
        return {
            'raw_recall': 1 - raw[2, 1] if raw is not None else 0,
            'raw_precision': 1 - raw[2, 0] if raw is not None else 1,
            'psf_recall': 1 - psf[2, 1] if psf is not None else 0,
            'psf_precision': 1 - psf[2, 0] if psf is not None else 1,
            'my_recall': 1 - my[2, 1] if my is not None else 0,
            'my_precision': 1 - my[2, 0] if my is not None else 1,
        }
    except:
        print(name)
        traceback.print_exc()


if __name__ == '__main__':
    files = [i.name for i in (wkdir / 'manual').glob('*.swc')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    files = [*filter(lambda f: tab.at[f, 'sparse'] == 1, files)]
    with Pool(14) as p:
        res = []
        for r in tqdm(p.imap(main, files), total=len(files)):
            res.append(r)
    tab = pd.DataFrame.from_records(res, index=files)
    tab.to_csv(wkdir / 'eval_psf.csv')


