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


class HidePrint:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def main(path: Path):
    man = next((wkdir / 'gold166' / path).parent.glob('*.swc'))
    my = wkdir / 'bigneuron_niend_app2' / path
    ada = wkdir / 'bigneuron_adathr_app2' / path
    mul = wkdir / 'bigneuron_multi_app2' / path
    guo = wkdir / 'bigneuron_guo_app2' /  path
    raw = wkdir / 'bigneuron_app2' / path
    try:
        with HidePrint():
            de = DistanceEvaluation(15)
            raw = de.run(raw, man) if raw.exists() else None
            my = de.run(my, man) if my.exists() else None
            guo = de.run(guo, man) if guo.exists() else None
            ada = de.run(ada, man) if ada.exists() else None
            mul = de.run(mul, man) if mul.exists() else None
        return {
            'raw_recall': 1 - raw[2, 1] if raw is not None else 0,
            'my_recall': 1 - my[2, 1] if my is not None else 0,
            'guo_recall': 1 - guo[2, 1] if guo is not None else 0,
            'ada_recall': 1 - ada[2, 1] if ada is not None else 0,
            'mul_recall': 1 - mul[2, 1] if mul is not None else 0,
            'raw_precision': 1 - raw[2, 0] if raw is not None else 1,
            'my_precision': 1 - my[2, 0] if my is not None else 1,
            'guo_precision': 1 - guo[2, 0] if guo is not None else 1,
            'ada_precision': 1 - ada[2, 0] if ada is not None else 1,
            'mul_precision': 1 - mul[2, 0] if mul is not None else 1,
        }
    except:
        print(path)
        traceback.print_exc()


if __name__ == '__main__':
    files = [i.relative_to(wkdir / 'bigneuron_niend_app2') for i in (wkdir / 'bigneuron_niend_app2').rglob('*.swc')]
    with Pool(14) as p:
        res = []
        for r in tqdm(p.imap(main, files), total=len(files)):
            res.append(r)
    tab = pd.DataFrame.from_records(res, index=files)
    tab.to_csv(wkdir / 'bigneuron_eval.csv')


