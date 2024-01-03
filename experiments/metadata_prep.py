from utils import swc_handler
import numpy as np


def get_name(in_path):
    tree = swc_handler.parse_swc(in_path)
    soma = np.array([t[2:5] for t in tree if t[6] == -1][0], dtype=int)
    br = in_path.stem.split('_')
    if br[0].startswith('p'):
        br = br[1]
    else:
        br = br[0]
    if br == '210254':
        br = '15257'
    return br, soma


if __name__ == '__main__':
    import pandas as pd
    import pickle
    from pathlib import Path
    from multiprocessing import Pool
    from tqdm import tqdm
    gs_dir = Path(r'Z:\SEU-ALLEN\Projects\fullNeurons\V2023_01_10\manual_final\All1891')
    crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
    files = [*gs_dir.glob('*.swc')]
    brains = []
    x = []
    y = []
    z = []
    with Pool(14) as p:
        for br, soma in tqdm(p.imap(get_name, files), total=len(files)):
            brains.append(br)
            x.append(soma[0])
            y.append(soma[1])
            z.append(soma[2])
    eval = pd.read_csv(r"D:\rectify\eval.csv", index_col=0)
    # with open(r"D:\rectify\time_use.pickle", 'rb') as f:
    #     times1 = pickle.load(f)
    # with open(r"D:\rectify\time_use_256.pickle", 'rb') as f:
    #     times2 = pickle.load(f)
    # crops = [i.stem + '.swc' for i in crop_path.glob('*.v3dpbd')]
    tab = pd.DataFrame({
        'gold_standard': [i.stem for i in files],
        'brain_id': brains,
        'soma_x': x,
        'soma_y': y,
        'soma_z': z,
    }, index=[f'{i[0]}_{i[1]}_{i[2]}_{i[3]}.swc' for i in zip(brains, x, y, z)])
    sparse = pd.read_csv(r"D:\rectify\filter.csv", index_col=0)
    tab['sparse'] = 0
    tab.loc[sparse.index, 'sparse'] = sparse.iloc[:, 0]
    # tab['1024_1024_256'] = 0.
    # tab.loc[crops, '1024_1024_256'] = times1
    # tab['256_256_256'] = 0.
    # tab.loc[crops, '256_256_256'] = times2

    tab['raw_LZMA_size'] = [(Path(r'D:\rectify\compressed\crop_8bit') / i).with_suffix('.tiff').stat().st_size for i in
                              tab.index]
    tab['NIEND_LZMA_size'] = [(Path(r'D:\rectify\compressed\my') / i).with_suffix('.tiff').stat().st_size for i in tab.index]
    with open(r"D:\rectify\compress_size.pickle", 'rb') as f:
        comp = pickle.load(f)
    tab['guo_LZMA_size'] = np.nan
    tab.loc[comp['guo_enh_8'][0], 'guo_LZMA_size'] = comp['guo_enh_8'][1]
    tab['multiscale_LZMA_size'] = np.nan
    tab.loc[comp['multiscale'][0], 'multiscale_LZMA_size'] = comp['multiscale'][1]
    tab['adathr_LZMA_size'] = np.nan
    tab.loc[comp['adathr8'][0], 'adathr_LZMA_size'] = comp['adathr8'][1]
    tab['raw_pbd_size'] = [(Path(r'D:\rectify\crop_8bit') / i).with_suffix('.v3dpbd').stat().st_size for i in tab.index]
    tab['NIEND_pbd_size'] = [(Path(r'D:\rectify\my') / i).with_suffix('.v3dpbd').stat().st_size for i in tab.index]
    tab['guo_pbd_size'] = [(Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\guo_enh_8") / i).
                               with_suffix('.v3dpbd').stat().st_size for i in tab.index]
    tab['multiscale_LZMA_size'] = np.nan
    tab.loc[comp['multiscale_pbd'][0], 'multiscale_LZMA_size'] = comp['multiscale_pbd'][1]
    tab['adathr_pbd_size'] = [(Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\adathr8") / i).
                               with_suffix('.v3dpbd').stat().st_size for i in tab.index]

    imgs = [i.with_suffix('.swc').name for i in Path(r"D:\rectify\my").rglob('*.v3dpbd')]
    imgs = [*filter(lambda f: tab.at[f, 'sparse'] == 1, imgs)]
    with open(r"D:\rectify\masking_guo_metric.pickle", 'rb') as f:
        raw, my, multi, ada, guo = pickle.load(f)
    imgs = [*filter(lambda x: (r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\multiscale" / Path(x).with_suffix('.v3draw')).exists(), imgs)]
    raw = np.transpose(raw)
    my = np.transpose(my)
    multi = np.transpose(multi)
    ada = np.transpose(ada)
    guo = np.transpose(guo)
    df = pd.DataFrame({
        'gold_standard': tab.loc[imgs, 'gold_standard'],
        'raw_sbc': raw[0], 'raw_ent': raw[1], 'raw_uni': raw[2], 'raw_rsd': raw[3],
        'adathr_sbc': ada[0], 'adathr_ent': ada[1], 'adathr_uni': ada[2], 'adathr_rsd': ada[3],
        'multiscale_sbc': multi[0], 'multiscale_ent': multi[1], 'multiscale_uni': multi[2], 'multiscale_rsd': multi[3],
        'guo_sbc': guo[0], 'guo_ent': guo[1], 'guo_uni': guo[2], 'guo_rsd': guo[3],
        'NIEND_sbc': my[0], 'NIEND_ent': my[1], 'NIEND_uni': my[2], 'NIEND_rsd': my[3],
    })

    eval.rename(columns={'mul_recall': 'multiscale_recall', 'ada_recall': 'adathr_recall', 'my_recall': 'NIEND_recall',
                         'mul_precision': 'multiscale_precision', 'ada_precision': 'adathr_precision', 'my_precision': 'NIEND_precision'}, inplace=True)
    eval = pd.concat([tab.loc[eval.index, 'gold_standard'], eval], axis=1)
    eval['NIEND_f1'] = 2 * (eval['NIEND_precision'] * eval['NIEND_recall']) / (eval['NIEND_precision'] + eval['NIEND_recall'] + .00001)
    eval['guo_f1'] = 2 * (eval['guo_precision'] * eval['guo_recall']) / (eval['guo_precision'] + eval['guo_recall'] + .00001)
    eval['multiscale_f1'] = (2 * (eval['multiscale_precision'] * eval['multiscale_recall']) /
                            (eval['multiscale_precision'] + eval['multiscale_recall'] + .00001))
    eval['adathr_f1'] = 2 * (eval['adathr_precision'] * eval['adathr_recall']) / (eval['adathr_precision'] + eval['adathr_recall'] + .00001)
    eval['NIEND_f1'] = 2 * (eval['NIEND_precision'] * eval['NIEND_recall']) / (eval['NIEND_precision'] + eval['NIEND_recall'] + .00001)

    with pd.ExcelWriter(r'D:\rectify\Supplementary_data.xlsx') as writer:
        tab.to_excel(writer, sheet_name='neuron_metadata', index=False,
                 columns=['gold_standard', 'brain_id', 'soma_x', 'soma_y', 'soma_z', 'sparse'])
        # tab.to_excel(writer, sheet_name='NIEND_time_use', index=False,
        #          columns=['gold_standard', '1024_1024_256', '256_256_256'])
        tab.to_excel(writer, sheet_name='compression_stats(byte)', index=False,
                 columns=['gold_standard', 'raw_LZMA_size', 'adathr_LZMA_size', 'multiscale_LZMA_size', 'guo_LZMA_size',
                          'NIEND_LZMA_size', 'raw_pbd_size', 'adathr_pbd_size', 'multiscale_LZMA_size', 'guo_pbd_size',
                          'NIEND_pbd_size'])
        df.to_excel(writer, sheet_name='quality_stats', index=False)
        eval.to_excel(writer, sheet_name='tracing_stats', index=False)
