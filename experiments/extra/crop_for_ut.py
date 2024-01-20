from pathlib import Path
from utils.v3d import terafly
import numpy as np
from v3dpy.loaders import Raw
from niend import simple_niend

tera_dir = Path(r'Z:\TeraconvertedBrain')
out_dir = Path(r'D:/rectify/tera_recon')


def main(name):
    parts = name.split('_')
    res_ord = 2
    block_sz = np.array([4096, 4096, 512]) // res_ord
    br = int(parts[0])
    x = int(parts[1]) // res_ord
    y = int(parts[2]) // res_ord
    z = int(parts[3]) // res_ord
    # get brain and brain terafly dir
    sub = [*tera_dir.glob(f'*{br}*')][0]
    res = [x for x in sub.iterdir() if x.is_dir()]
    res_sz = [int(str(x).split('x')[1]) for x in res]
    ord = np.argsort(res_sz)

    # get soma coord
    coord = np.array([x, y, z])
    out_path1 = out_dir / f'{name}_raw.v3draw'
    out_path2 = out_dir / f'{name}_niend.v3draw'

    in_path = sub / res[ord[len(ord) - res_ord]]
    st = coord - block_sz // 2
    ed = coord + block_sz // 2
    arr = terafly.Interface.get_subvolume(str(in_path), st[0], ed[0], st[1], ed[1], st[2], ed[2])
    img1 = (arr * (255 / arr.max())).astype('uint8')
    Raw().save(out_path1, np.array([img1]))
    img2 = simple_niend(arr, 10, 5, 1).astype('uint16') * 255
    Raw().save(out_path2, np.array([img2]))


if __name__ == '__main__':
    cand = ['17302_15030_27059_4032', '17302_16210_40007_5418', '18457_11620_14084_5420']
    for i in cand:
        main(i)



