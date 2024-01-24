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


def main(name):
    man = wkdir / 'manual' / name
    my = wkdir / 'my_app2' / name
    bit8 = wkdir / 'ablation' / '8bit_app2' / name
    high = wkdir / 'ablation' / 'high_app2' / name
    clip = wkdir / 'ablation' / 'clip_app2' / name
    ff = wkdir / 'ablation' / 'feedforward_app2' / name
    vert = wkdir / 'ablation' / 'vertical_app2' / name
    wvlet = wkdir / 'ablation' / 'wvlet_app2' / name
    try:
        with HidePrint():
            de = DistanceEvaluation(15)
            my = de.run(my, man) if my.exists() else None
            bit8 = de.run(bit8, man) if bit8.exists() else None
            high = de.run(high, man) if high.exists() else None
            ff = de.run(ff, man) if ff.exists() else None
            vert = de.run(vert, man) if vert.exists() else None
            clip = de.run(clip, man) if clip.exists() else None
            wvlet = de.run(wvlet, man) if wvlet.exists() else None
        return {
            'my_recall': 1 - my[2, 1] if my is not None else 0,
            'bit8_recall': 1 - bit8[2, 1] if bit8 is not None else 0,
            'high_recall': 1 - high[2, 1] if high is not None else 0,
            'ff_recall': 1 - ff[2, 1] if ff is not None else 0,
            'vert_recall': 1 - vert[2, 1] if vert is not None else 0,
            'clip_recall': 1 - clip[2, 1] if clip is not None else 0,
            'wvlet_recall': 1 - wvlet[2, 1] if wvlet is not None else 0,
            'my_precision': 1 - my[2, 0] if my is not None else 1,
            'bit8_precision': 1 - bit8[2, 0] if bit8 is not None else 1,
            'high_precision': 1 - high[2, 0] if high is not None else 1,
            'ff_precision': 1 - ff[2, 0] if ff is not None else 1,
            'vert_precision': 1 - vert[2, 0] if vert is not None else 1,
            'clip_precision': 1 - clip[2, 0] if clip is not None else 1,
            'wvlet_precision': 1 - wvlet[2, 0] if wvlet is not None else 1,
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
    tab.to_csv(wkdir / 'ablation' / 'eval.csv')


