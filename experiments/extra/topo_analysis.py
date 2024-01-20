from utils import swc_handler
from utils.morphology import Morphology
from pathlib import Path
from sklearn.neighbors import KDTree
import numpy as np


wkdir = Path('d:/rectify')


def detect_breaks(tree, gs):
    count = 0
    kd = KDTree([t[2:5] for t in tree])
    morph1 = Morphology(tree)
    morph2 = Morphology(gs)
    seg_tree, seg_dict = morph2.convert_to_topology_tree()
    for k, v in seg_dict.items():
        if len(v) < 2:
            continue
        t1, t2 = v[0], v[-1]
        dists, inds = kd.query([morph2.pos_dict[t1][2:5], morph2.pos_dict[t2][2:5]])
        if (dists > 5).any():
            continue
        trail1 = [tree[inds[0][0]][0]]
        trail2 = [tree[inds[1][0]][0]]
        while trail1[-1] != -1:
            trail1.append(morph1.pos_dict[trail1[-1]][6])
        while trail2[-1] != -1:
            trail2.append(morph1.pos_dict[trail2[-1]][6])
        trail1.reverse()
        trail2.reverse()
        for i, t in enumerate(trail1):
            if i >= len(trail2):
                break
            if t != trail2[i]:
                len1 = len2 = 0
                for j in range(i + 1, len(trail1)):
                    len1 += np.linalg.norm(np.array(morph1.pos_dict[trail1[j]][2:5]) - morph1.pos_dict[trail1[j - 1]][2:5])
                for j in range(i + 1, len(trail2)):
                    len1 += np.linalg.norm(np.array(morph1.pos_dict[trail2[j]][2:5]) - morph1.pos_dict[trail2[j - 1]][2:5])
                for j in range(len(v) - 1):
                    len2 += np.linalg.norm(np.array(morph2.pos_dict[v[j]][2:5]) - morph2.pos_dict[v[j + 1]][2:5])
                if len1 - len2 > 10 and len1 / len2 > 1.2:
                    count += 1
                break
    return count


def detect_fusion(tree, gs):
    count = 0
    morph1 = Morphology(tree)
    lengths1 = morph1.calc_frag_lengths()[0]
    path_dict1 = morph1.get_path_idx_dict()
    path_dists1 = morph1.get_path_len_dict(path_dict1, lengths1)

    morph2 = Morphology(gs)
    lengths2 = morph2.calc_frag_lengths()[0]
    path_dict2 = morph2.get_path_idx_dict()
    path_dists2 = morph2.get_path_len_dict(path_dict2, lengths2)

    kd = KDTree([t[2:5] for t in tree])

    crits = list(morph2.bifurcation | morph2.multifurcation | morph2.tips)
    dists, inds = kd.query([morph2.pos_dict[i][2:5] for i in crits])
    for d, i, c in zip(dists, inds, crits):
        d = d[0]
        i = tree[i[0]][0]
        if morph2.pos_dict[c][6] == -1 or d > 5:
            continue
        pd1 = path_dists1[i]
        pd2 = path_dists2[c]
        if abs(pd1 - pd2) > 10 and (pd1 / pd2 > 1.2 or pd2 / pd1 > 1.2):
            count += 1
    return count


def detect_reverse(tree, gs):
    kd = KDTree([t[2:5] for t in gs])
    dist, ind = kd.query([t[2:5] for t in tree], 1, dualtree=True)
    morph1 = Morphology(tree)
    morph2 = Morphology(gs)
    para = rev = 0
    for d, i, t1 in zip(dist, ind, tree):
        d = d[0]
        i = i[0]
        if d > 5:
            continue
        t2 = gs[i]
        p1 = t1[6]
        p2 = t2[6]
        if p1 == -1 or p2 == -1:
            continue
        vec1 = np.array(t1[2:5]) - morph1.pos_dict[p1][2:5]
        vec2 = np.array(t2[2:5]) - morph2.pos_dict[p2][2:5]
        len1 = np.linalg.norm(vec1)
        if vec1.dot(vec2) > 0:
            para += len1
        else:
            rev += len1
    return para, rev


def pathdist_branchorder(tree, gs):
    kd = KDTree([t[2:5] for t in tree])
    morph1 = Morphology(tree)
    morph2 = Morphology(gs)
    lengths = morph1.calc_frag_lengths()[0]
    path_dict = morph1.get_path_idx_dict()
    path_dists = morph1.get_path_len_dict(path_dict, lengths)
    crits = list(morph2.bifurcation | morph2.multifurcation)
    dists, inds = kd.query([morph2.pos_dict[i][2:5] for i in crits])

    seg_tree, seg_dict = morph2.convert_to_topology_tree()
    bo = {}
    mo = Morphology(seg_tree)
    for t in seg_tree:
        p = t[6]
        o = 0
        while p != -1:
            p = mo.pos_dict[p][6]
            o += 1
        bo[t[0]] = o

    out = []
    for d, i, c in zip(dists, inds, crits):
        d = d[0]
        i = tree[i[0]][0]
        if d > 5 or morph2.pos_dict[c][1] == 2:
            continue
        out.append((bo[c], path_dists[i]))
    return out


wkdir = Path('d:/rectify')
guo_dir = Path(r'Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\guo8_app2')
adathr_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\adathr_app2")
multi_dir = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\rectify_1891\multiscale_app2")


def main(name):
    try:
        man = swc_handler.parse_swc(wkdir / 'manual' / name)
        my = swc_handler.parse_swc(wkdir / 'my_app2' / name)
        ada = swc_handler.parse_swc(adathr_dir / name)
        mul = swc_handler.parse_swc(multi_dir / name)
        guo = swc_handler.parse_swc(guo_dir / name)
        raw = swc_handler.parse_swc(wkdir / 'raw_app2' / name)

        ans = {}

        ans['gs_pdsholl'] = pathdist_branchorder(man, man)

        ans['niend'] = {
            'breaks': detect_breaks(my, man),
            'fusion': detect_fusion(my, man),
            'reverse': detect_reverse(my, man),
            'pdsholl': pathdist_branchorder(my, man)
        }

        ans['ada'] = {
            'breaks': detect_breaks(ada, man),
            'fusion': detect_fusion(ada, man),
            'reverse': detect_reverse(ada, man),
            'pdsholl': pathdist_branchorder(ada, man)
        }

        ans['multi'] = {
            'breaks': detect_breaks(mul, man),
            'fusion': detect_fusion(mul, man),
            'reverse': detect_reverse(mul, man),
            'pdsholl': pathdist_branchorder(mul, man)
        }

        ans['guo'] = {
            'breaks': detect_breaks(guo, man),
            'fusion': detect_fusion(guo, man),
            'reverse': detect_reverse(guo, man),
            'pdsholl': pathdist_branchorder(guo, man)
        }

        ans['raw'] = {
            'breaks': detect_breaks(raw, man),
            'fusion': detect_fusion(raw, man),
            'reverse': detect_reverse(raw, man),
            'pdsholl': pathdist_branchorder(raw, man)
        }

        return ans
    except:
        return None


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm
    import pandas as pd
    files = [i.name for i in (wkdir / 'manual').glob('*.swc')]
    tab = pd.read_csv(wkdir / 'filter.csv', index_col=0)
    files = [*filter(lambda f: tab.at[f, 'sparse'] == 1, files)]
    res = []
    with Pool(12) as p:
        for i in tqdm(p.imap(main, files), total=len(files)):
            res.append(i)
    import pickle
    with open(wkdir / 'topo_eval.pickle', 'wb') as f:
        pickle.dump(res, f)

