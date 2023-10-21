# filter for human
from pathlib import Path
from multiprocessing import Pool

from v3dpy.loaders import PBD
from neuron_image_denoise.filter import *
from tqdm import tqdm
import matplotlib.pyplot as plt
from utils.swc_handler import parse_swc
from utils import morphology

wkdir = Path(r"D:\rectify")
crop_path = wkdir / 'human_crop'
filt_path = wkdir / 'my_human'
out_path = wkdir / 'human_mip'
out_path.mkdir(exist_ok=True)


class NeuriteArbors:
    def __init__(self, swcfile):
        tree = parse_swc(swcfile)
        self.morph = morphology.Morphology(tree)
        self.morph.get_critical_points()

    def get_paths_of_specific_neurite(self, mip='z'):
        """
        Tip: set
        """
        if mip == 'z':
            idx1, idx2 = 2, 3
        elif mip == 'x':
            idx1, idx2 = 3, 4
        elif mip == 'y':
            idx1, idx2 = 2, 4
        else:
            raise NotImplementedError

        paths = []
        for tip in self.morph.tips:
            path = []
            node = self.morph.pos_dict[tip]
            # if node[1] not in type_id: continue
            path.append([node[idx1], node[idx2]])
            while node[6] in self.morph.pos_dict:
                pid = node[6]
                pnode = self.morph.pos_dict[pid]
                path.append([pnode[idx1], pnode[idx2]])
                node = self.morph.pos_dict[pid]

            paths.append(np.array(path))

        return paths

    def plot_morph_mip(self, xxyy=None, mip='z', color='r'):
        paths = self.get_paths_of_specific_neurite(mip=mip)

        for path in paths:
            plt.plot(path[:, 0], path[:, 1], color=color, linewidth=.2)


def main(file):
    raw = PBD().load(crop_path / file.name)[0].max(axis=0)
    my = PBD().load(filt_path / file.name)[0].max(axis=0)
    plt.figure()
    plt.subplot(1, 3, 1)
    plt.imshow(raw)
    plt.xticks([])
    plt.yticks([])
    plt.title('raw')

    plt.subplot(1, 3, 2)
    plt.imshow(my)
    plt.xticks([])
    plt.yticks([])
    plt.title('my')

    plt.subplot(1, 3, 3)
    p = [*filt_path.glob(f'{file.name}*_app2.swc')][0]
    tree = NeuriteArbors(p)

    plt.imshow(my)
    plt.xticks([])
    plt.yticks([])
    plt.title('app2')
    tree.plot_morph_mip()
    plt.savefig((out_path / file.name).with_suffix('.png'), bbox_inches='tight', dpi=200)
    plt.close()


if __name__ == '__main__':
    arglist = []
    for f in crop_path.rglob('*.v3dpbd'):
        arglist.append(f)

    with Pool(12) as p:
        for res in tqdm(p.imap(main, arglist), total=len(arglist)): pass


