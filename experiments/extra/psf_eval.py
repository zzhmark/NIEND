# evaluate different reconstruction against gold standard

from neuron_quality.metrics import DistanceEvaluation
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


class HidePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def main(name: str):
    man = wkdir / 'manual' / name
    my = psf_dir / name
    try:
        with HidePrint():
            de = DistanceEvaluation(15)
            my = de.run(my, man) if my.exists() else None
        return {
            'recall': 1 - my[2, 1] if my is not None else 0,
            'precision': 1 - my[2, 0] if my is not None else 1,
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


