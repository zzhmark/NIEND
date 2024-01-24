from v3dpy.loaders import PBD
from pathlib import Path
import sys
import numpy as np




if __name__ == '__main__':
    from multiprocessing import Pool
    in_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    outpath = out_dir / in_path.name
    if outpath.exists():
        exit()

    img = PBD().load(in_path)
    bd = 8
    
    img[0, :bd] = 0
    img[0, -bd:] = 0
    img[0, :, :bd] = 0
    img[0, :, -bd:] = 0
    img[..., :bd] = 0
    img[..., -bd:] = 0
    
    PBD().save(outpath, img)
    
    