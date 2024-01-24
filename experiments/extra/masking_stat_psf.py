import numpy as np
from scipy.stats import entropy


def stats(sg, bg, stats):
    avg, std = stats
    sbc = np.median(sg) / (np.median(bg) + 1)
    hist = np.histogram((bg - avg) / std, 100, density=True)[0]
    ent = entropy(hist)
    uni = (hist**2).mean()
    rsd = sg.std() / (np.median(sg) + 1)
    return sbc, ent, uni, rsd


def main(di):
    raw = stats(*di['raw'])
    psf = stats(*di['psf'])
    my = stats(*di['my'])
    return di['name'], raw, psf, my


if __name__ == '__main__':
    import pickle
    from pathlib import Path
    from multiprocessing import Pool
    from tqdm import tqdm

    wkdir = Path(r"D:\rectify")
    with open(wkdir / 'psf_masking_final.pickle', 'rb') as f:
        masking = pickle.load(f)
    names = []
    auc_raw = []
    auc_my = []
    auc_psf = []
    with Pool(14) as p:
        for name, raw, psf, my in tqdm(p.imap(main, masking), total=len(masking)):
            names.append(name)
            auc_raw.append(raw)
            auc_my.append(my)
            auc_psf.append(psf)

    with open(wkdir / 'psf_masking_guo_metric.pickle', 'wb') as f:
        pickle.dump((auc_raw, auc_psf, auc_my, names), f)
