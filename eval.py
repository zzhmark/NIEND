from neuron_quality.metrics import DistanceEvaluation
import pandas as pd
from pathlib import Path
from multiprocessing import Pool
import sys
import os
import traceback
from tqdm import tqdm

wkdir = Path(r"D:\rectify")

class HidePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def main(name):
    man = wkdir / 'manual' / name
    my = wkdir / 'my_app2' / name
    raw = wkdir / 'raw_app2' / name
    try:
        with HidePrint():
            de = DistanceEvaluation(5)
            raw = de.run(raw, man) if raw.exists() else None
            my = de.run(my, man) if my.exists() else None
        return {
            'raw_recall': 1 - raw[2, 1] if raw is not None else 0,
            'proc_recall': 1 - my[2, 1] if my is not None else 0,
            'raw_precision': 1 - raw[2, 0] if raw is not None else 1,
            'proc_precision': 1 - my[2, 0] if my is not None else 1
        }
    except:
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
    tab.to_csv(wkdir / 'eval.csv')


