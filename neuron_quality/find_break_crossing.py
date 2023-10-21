#!/usr/bin/env python

# ================================================================
#   Copyright (C) 2022 Yufeng Liu (Braintell, Southeast University). All rights reserved.
#   
#   Filename     : find_break_crossing.py
#   Author       : Yufeng Liu
#   Date         : 2022-04-01
#   Description  : 
#
# ================================================================
import numpy as np
from scipy.spatial import distance_matrix

from utils.math_utils import calc_included_angles_from_vectors
from morph_topo.morphology import Morphology


def find_point_by_distance(pt, anchor_idx, is_parent, morph, dist, return_center_point=True, epsilon=1e-7,
                           spacing=(1., 1., 1.), stop_by_branch=True, only_tgt_pt=True, radius=False, pt_rad=None):
    """ 
    Find the point of exact `dist` to the start pt on tree structure. args are:
    - pt: the start point, [coordinate]
    - anchor_idx: the first node on swc tree to trace, first child or parent node
    - is_parent: whether the anchor_idx is the parent of `pt`, otherwise child. 
                 if a furcation points encounted, then break
    - morph: Morphology object for current tree
    - dist: distance threshold
    - return_center_point: whether to return the point with exact distance or
                 geometric point of all traced nodes
    - epsilon: small float to avoid zero-division error 
    """

    d = 0
    ci = pt
    pts = [pt]
    ri = pt_rad
    rad = [pt_rad]
    while d < dist:
        try:
            cc = np.array(morph.pos_dict[anchor_idx][2:5])
            rr = morph.pos_dict[anchor_idx][5]
        except KeyError:
            print(f"Parent/Child node not found within distance: {dist}")
            break
        d0 = np.linalg.norm((ci - cc) * spacing)
        d += d0
        if d < dist:
            ci = cc  # update coordinates
            ri = rr
            pts.append(cc)
            rad.append(rr)
            if is_parent:
                anchor_idx = morph.pos_dict[anchor_idx][6]
                if stop_by_branch and len(morph.child_dict[anchor_idx]) > 1:
                    break
            else:
                if (anchor_idx not in morph.child_dict) or (stop_by_branch and (len(morph.child_dict[anchor_idx]) > 1)):
                    break
                else:
                    anchor_idx = morph.child_dict[anchor_idx][0]

    # interpolate to find the exact point
    dd = d - dist
    if dd < 0:
        pt_a = cc
    else:
        dcur = np.linalg.norm((cc - ci) * spacing)
        assert (dcur - dd >= 0)
        pt_a = ci + (cc - ci) * (dcur - dd) / (dcur + epsilon)
        if radius:
            r_a = ri + (rr - ri) * (dcur - dd) / (dcur + epsilon)
            rad.append(r_a)
        pts.append(pt_a)

    if return_center_point:
        pt_a = np.mean(pts, axis=0)

    ret = pt_a
    if not only_tgt_pt:
        ret = ret, pts
    if radius:
        ret = *ret, rad
    return ret


class BreakFinder(object):
    def __init__(self, morph, soma_radius=30, dist_thresh=4.0, line_length=5.0, angle_thresh=90.,
                 spacing=np.array([1., 1., 1.])):
        self.morph = morph

        self.soma_radius = soma_radius
        self.dist_thresh = dist_thresh
        self.line_length = line_length
        self.angle_thresh = angle_thresh
        self.spacing = spacing

    def find_break_pairs(self):
        ntips = len(self.morph.tips)

        # filter tips near soma
        tip_list = []
        sc = np.array(self.morph.pos_dict[self.morph.idx_soma][2:5])
        for tip in self.morph.tips:
            ci = np.array(self.morph.pos_dict[tip][2:5])
            dist = np.linalg.norm((sc - ci) * self.spacing)
            if dist < self.soma_radius:
                continue
            tip_list.append(tip)

        ret = {}
        for idx1, tip1 in enumerate(tip_list):
            c1 = np.array(self.morph.pos_dict[tip1][2:5])
            for idx2 in range(idx1 + 1, len(tip_list)):
                tip2 = tip_list[idx2]
                c2 = np.array(self.morph.pos_dict[tip2][2:5])
                # distance criterion
                dist = np.linalg.norm((c1 - c2) * self.spacing)
                if dist > self.dist_thresh: continue

                # estimate the fiber distance
                pid1 = self.morph.pos_dict[tip1][6]  # parent id for tip1
                pt1 = find_point_by_distance(c1, pid1, True, self.morph, self.line_length, False)
                pid2 = self.morph.pos_dict[tip2][6]
                pt2 = find_point_by_distance(c2, pid2, True, self.morph, self.line_length, False)
                # angle 
                v1 = pt1 - c1
                v2 = pt2 - c2
                ang = calc_included_angles_from_vectors(v1, v2)[0]
                if ang > self.angle_thresh:
                    ret[(tip1, tip2)] = (ang, dist)
                # print(tip1, tip2, ang, dist)

        return ret

    def find_break_pairs_by_distances(self):
        """
        find potential tip pair based on pair-wise distance only, so it can be accelerated
        with more compact vectorization
        """
        sc = np.array(self.morph.pos_dict[self.morph.idx_soma][2:5])
        tip_coords = np.array([self.morph.pos_dict[tip][2:5] for tip in self.morph.tips])
        tip_indices = np.array([self.morph.pos_dict[tip][0] for tip in self.morph.tips])
        ts_vec = (tip_coords - sc) * self.spacing
        ts_dists = np.linalg.norm(ts_vec, axis=1)

        # filter out tips near soma
        tip_out_mask = ts_dists > self.soma_radius
        tip_out_indices = tip_indices[tip_out_mask]
        tip_out_coords = tip_coords[tip_out_mask]

        # pairwise distances
        pdists = distance_matrix(tip_out_coords, tip_out_coords)
        ids1, ids2 = np.nonzero(pdists > self.dist_thresh)
        ret = {}
        for i, j in zip(ids1, ids2):
            try:
                ret[tip_out_indices[i]].append(tip_out_indices[j])
            except KeyError:
                ret[tip_out_indices[i]] = [tip_out_indices[j]]
        return ret


class CrossingFinder(object):
    def __init__(self, morph: Morphology, soma_radius=30., dist_thresh=3., spacing=np.array([1., 1., 1.]), epsilon=1e-7):
        self.morph = morph
        self.soma_radius = soma_radius
        self.dist_thresh = dist_thresh
        self.spacing = spacing
        self.epsilon = epsilon

    def find_crossing_pairs(self):
        pairs = []
        points = []
        morph = self.morph

        cs = np.array(morph.pos_dict[morph.idx_soma][2:5])
        pset = set()
        visited = set()
        for tid in morph.tips:
            idx = tid
            pre_tip_id = None
            cur_tip_id = None
            while idx != morph.idx_soma and idx != -1:
                if idx in morph.child_dict and len(morph.child_dict[idx]) >= 2:
                    pre_tip_id = cur_tip_id
                    cur_tip_id = idx
                    if pre_tip_id is not None:
                        if pre_tip_id in visited:
                            break
                        visited.add(pre_tip_id)
                        c0 = np.array(morph.pos_dict[cur_tip_id][2:5])
                        c1 = np.array(morph.pos_dict[pre_tip_id][2:5])
                        if np.linalg.norm((c0 - cs) * self.spacing) > self.soma_radius:
                            dist = np.linalg.norm((c0 - c1) * self.spacing)
                            # for fear that a pair can point to soma
                            ct = np.mean([morph.pos_dict[cur_tip_id][2:5], morph.pos_dict[pre_tip_id][2:5]], axis=0)
                            if np.linalg.norm(ct - morph.pos_dict[morph.idx_soma][2:5]) > self.epsilon and \
                                    dist < self.dist_thresh:
                                pairs.append((pre_tip_id, cur_tip_id, dist))
                                pset.add(pre_tip_id)
                                pset.add(cur_tip_id)
                idx = morph.pos_dict[idx][6]

            for idx, ch in morph.child_dict.items():
                if len(ch) > 2 and idx not in pset and \
                        np.linalg.norm((morph.pos_dict[idx][2:5] - cs) * self.spacing) > self.soma_radius:
                    points.append(idx)
                    pset.add(idx)

        # print(f'Dist: {dists.mean():.2f}, {dists.std():.2f}, {dists.max():.2f}, {dists.min():.2f}')
        # for pair in pairs:
        #    print(f'idx1 / idx2 and dist: {pair[0]} / {pair[1]} / {pair[2]}')
        print(f'Number of crossing and crossing-like: {len(points)} / {len(pairs)}')
        return points, pairs

    def find_mega_crossing(self, include_bifurcation=False):
        chains = []
        topo_tree, seg_dict = self.morph.convert_to_topology_tree()
        topo_morph = Morphology(topo_tree)
        dists = topo_morph.get_distances_to_soma(self.spacing)
        visited = dict.fromkeys(topo_morph.pos_dict.keys(), False)
        branch = topo_morph.bifurcation | topo_morph.multifurcation
        for tid in topo_morph.tips:
            chain = []
            if tid == topo_morph.p_soma:
                continue
            idx = topo_morph.pos_dict[tid][6]       # starting from the last branch
            while idx != topo_morph.p_soma:
                if chain:
                    v = np.array([topo_morph.pos_dict[chain[-1]][2:5]] + [self.morph.pos_dict[n][2:5] for n in seg_dict[chain[-1]]] + [topo_morph.pos_dict[idx][2:5]])
                    if np.linalg.norm((v[1:] - v[:-1]) * self.spacing, axis=-1).sum() > self.dist_thresh or \
                            dists[topo_morph.index_dict[idx]] <= self.soma_radius or idx not in branch:
                        if len(chain) > 1 or chain[0] in topo_morph.multifurcation or include_bifurcation:
                            chains.append(chain)
                        chain = []
                        if visited[idx]:
                            break
                if dists[topo_morph.index_dict[idx]] > self.soma_radius and idx in branch:
                    chain.append(idx)
                visited[idx] = True
                idx = topo_morph.pos_dict[idx][6]
            if len(chain) > 1 or chain and (chain[0] in topo_morph.multifurcation or include_bifurcation):
                chains.append(chain)
        # merge
        return [set.union(*[set(t) for t in chains if t[-1] == head]) for head in np.unique([i[-1] for i in chains])]
