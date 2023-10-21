# evaluate different reconstruction against gold standard

from neuron_quality.metrics import DistanceEvaluation
import pandas as pd
from pathlib import Path
from multiprocessing import Pool
import sys
import os
import traceback
from tqdm import tqdm
import metrics_delin as md

wkdir = Path(r"D:\rectify")
guo_dir = Path(r'Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\guo8_app2')
adathr_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\adathr_app2")
multi_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\multiscale_app2")


def main(name):
    def optj(gt, rc, name):
        try:
            f1 = md.opt_g(gt, rc, spacing=10,
                                  dist_limit=300,
                                  dist_matching=25,
                                  N=50,  # to speed up this script
                                  verbose=False)[0] if rc is not None else 0
        except:
            f1 = None
        return {
            # f'{name}_f1': f1,
            # f'{name}_precision': p,
            # f'{name}_recall': r
            name: f1
        }

    man = wkdir / 'manual' / name
    my = wkdir / 'my_app2' / name
    ada = adathr_dir / name
    mul = multi_dir / name
    guo = guo_dir / name
    raw = wkdir / 'raw_app2' / name

    man = md.load_graph_swc(wkdir / 'manual' / name) if man.exists() else None
    my = md.load_graph_swc(wkdir / 'my_app2' / name) if my.exists() else None
    ada = md.load_graph_swc(adathr_dir / name) if ada.exists() else None
    mul = md.load_graph_swc(multi_dir / name) if mul.exists() else None
    guo = md.load_graph_swc(guo_dir / name) if guo.exists() else None
    raw = md.load_graph_swc(wkdir / 'raw_app2' / name) if raw.exists() else None
    try:
        return {
            **optj(man, my, 'my'),
            **optj(man, ada, 'ada'),
            **optj(man, mul, 'mul'),
            **optj(man, guo, 'guo'),
            **optj(man, raw, 'raw')
        }
    except:
        print(name)
        traceback.print_exc()


if __name__ == '__main__':
    files = [i.name for i in (wkdir / 'manual').glob('*.swc')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    files = [*filter(lambda f: tab.at[f, 'sparse'] == 1, files)]
    # print(main('17302_13811_42025_3130.swc'))
    with Pool(14) as p:
        # res = []
        avg_guo = 0
        count_guo = 0
        avg_raw = 0
        count_raw = 0
        avg_ada = 0
        count_ada = 0
        avg_mul = 0
        count_mul = 0
        avg_my = 0
        count_my = 0
        for r in tqdm(p.imap(main, files), total=len(files)):
            # res.append(r)
            if r['guo'] is not None:
                count_guo += 1
                avg_guo += r['guo']
            if r['mul'] is not None:
                count_mul += 1
                avg_mul += r['mul']
            if r['my'] is not None:
                count_my += 1
                avg_my += r['my']
            if r['ada'] is not None:
                count_ada += 1
                avg_ada += r['ada']
            if r['raw'] is not None:
                count_raw += 1
                avg_raw += r['raw']
    print(f'raw: {avg_raw / count_raw}')
    print(f'ada: {avg_ada / count_ada}')
    print(f'mul: {avg_mul / count_mul}')
    print(f'guo: {avg_guo / count_guo}')
    print(f'my: {avg_my / count_my}')
    # tab = pd.DataFrame.from_records(res, index=files)
    # tab.to_csv(wkdir / 'optj_f1.csv')


