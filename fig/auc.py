import numpy as np
from sklearn.metrics import roc_auc_score


def main(di):

    raw = roc_auc_score([True] * len(di['raw'][0]) + [False] * len(di['raw'][1]), np.hstack(di['raw']))
    my = roc_auc_score([True] * len(di['my'][0]) + [False] * len(di['my'][1]), np.hstack(di['my']))
    ada = roc_auc_score([True] * len(di['ada'][0]) + [False] * len(di['ada'][1]), np.hstack(di['ada']))
    multi = roc_auc_score([True] * len(di['multi'][0]) + [False] * len(di['multi'][1]), np.hstack(di['multi']))
    guo = roc_auc_score([True] * len(di['guo'][0]) + [False] * len(di['guo'][1]), np.hstack(di['guo']))
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

    with open(wkdir / 'masking_auc.pickle', 'wb') as f:
        pickle.dump((auc_raw, auc_my, auc_multi, auc_ada, auc_guo), f)
