import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import seaborn as sns


if __name__ == '__main__':
    wkdir = Path('D:/rectify')
    df = pd.read_csv(wkdir / 'eval.csv', index_col=0)
    df['raw_f1'] = 2 * (df['raw_precision'] * df['raw_recall']) / (df['raw_precision'] + df['raw_recall'])
    df['proc_f1'] = 2 * (df['proc_precision'] * df['proc_recall']) / (df['proc_precision'] + df['proc_recall'])
    df['diff_f1'] = df['proc_f1'] - df['raw_f1']

    # plot f1
    # plt.violinplot(df[['raw_f1', 'proc_f1', 'diff_f1']].to_numpy())
    # x = []
    # for i, v in enumerate(['raw_f1', 'proc_f1', 'diff_f1']):
    #     v = df[v].to_numpy()
    #     x.append(np.random.normal(i + 1, 0.08, len(v)))
    #     plt.scatter(x[-1], v, s=0.1)
    # plt.xticks([1, 2, 3], ['raw', 'proc', 'gain'])
    # plt.title(f'F1 score on {len(df)} sparse neurons')
    dist = df[['raw_f1', 'proc_f1']]
    dist = dist.melt(value_vars=dist.columns, var_name='var', value_name='f1')
    sns.displot(dist, x='f1', kind='kde', hue='var', fill=True)
    plt.savefig(wkdir / 'f1.png')
    plt.close()


    # plot curve
    bin = 25
    bins = [i/bin for i in range(bin + 1)]
    plt.figure()
    raw = df[['raw_precision', 'raw_recall']].sort_values('raw_recall')
    # raw_ap = 0
    # for i in range(1, len(raw)):
    #     raw_ap += raw['raw_precision'].iat[i] * (raw['raw_recall'].iat[i] - raw['raw_recall'].iat[i - 1])
    raw['bin'] = pd.qcut(raw['raw_recall'], q=bins)
    raw = pd.pivot_table(raw, index='bin')

    proc = df[['proc_precision', 'proc_recall']].sort_values('proc_recall')
    # proc_ap = 0
    # for i in range(1, len(proc)):
    #     proc_ap += proc['proc_precision'].iat[i] * (proc['proc_recall'].iat[i] - proc['proc_recall'].iat[i - 1])
    proc['bin'] = pd.qcut(proc['proc_recall'], q=bins)
    proc = pd.pivot_table(proc, index='bin')

    bins = [i + .5 / bin for i in bins][:-1]
    plt.plot(bins, raw['raw_precision'])
    plt.plot(bins, proc['proc_precision'])
    plt.legend(['raw', 'proc'])
    # plt.legend([f'raw(AP={raw_ap:{1}.{2}})', f'proc(AP={proc_ap:{1}.{2}})'])
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.title(f'PR curve on {len(df)} sparse neurons')
    plt.savefig(wkdir / 'pr.png')
    plt.close()
