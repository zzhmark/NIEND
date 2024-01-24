import numpy as np
from scipy.stats import entropy


def stats(sg, bg, stats):
    avg, std = stats
    # sg = sg[sg >= np.percentile(sg, 10)]
    # bg = bg[bg <= np.percentile(bg, 90)]
    # m = max(sg.max(), bg.max())
    # bg = bg / m
    # sg = sg / m
    sbc = np.median(sg) / (np.median(bg) + 1)
    hist = np.histogram((bg - avg) / std, 100, density=True)[0]
    ent = entropy(hist)
    uni = (hist**2).mean()
    rsd = sg.std() / (np.median(sg) + 1)
    return sbc, ent, uni, rsd


def main(di):
    raw = stats(*di['raw'])
    my = stats(*di['my'])
    ada = stats(*di['ada'])
    multi = stats(*di['multi'])
    guo = stats(*di['guo'])
    return raw, my, ada, multi, guo


if __name__ == '__main__':
    import pickle
    from pathlib import Path
    from multiprocessing import Pool
    from tqdm import tqdm

    wkdir = Path(r"D:\rectify")
    with open(wkdir / 'masking_final.pickle', 'rb') as f:
        masking = pickle.load(f)
    auc_raw = []
    auc_my = []
    auc_multi = []
    auc_ada = []
    auc_guo = []
    with Pool(14) as p:
        for raw, my, ada, multi, guo in tqdm(p.imap(main, masking), total=len(masking)):
            auc_raw.append(raw)
            auc_my.append(my)
            auc_multi.append(multi)
            auc_ada.append(ada)
            auc_guo.append(guo)

    with open(wkdir / 'masking_guo_metric.pickle', 'wb') as f:
        pickle.dump((auc_raw, auc_my, auc_multi, auc_ada, auc_guo), f)
