import numpy as np
from sklearn.decomposition import NMF
from pathlib import Path
from v3dpy.loaders import PBD
from utils.file_io import save_image

wkdir = Path(r"D:\rectify")
crop_path = Path(r"Z:\SEU-ALLEN\Users\zuohan\trans\crop1891\1st")
out_dir = wkdir / 'nmf'


def main(img_path: Path):
    image_data = PBD().load(img_path)[0]

    # Assuming `image_data` is a 3D numpy array with shape (num_slices, height, width)
    # where num_slices is the number of image slices along the z-axis

    # Step 1: Average every 10 slices along the z-axis
    averaged_slices = np.mean(image_data.reshape(-1, 16, *image_data.shape[1:]), axis=1)

    # Step 2: Unfold the averaged slices into 1D vectors
    unfolded_vectors = averaged_slices.reshape(averaged_slices.shape[0], -1)

    # Step 3: Construct the NMF model with three components
    nmf_model = NMF(n_components=3, init='nndsvd', random_state=0)

    # Step 4: Fit the model to the unfolded vectors
    W = nmf_model.fit_transform(unfolded_vectors)  # Basis matrix
    H = nmf_model.components_  # Coefficient matrix

    # Step 5: The first component is used as the background
    background_component = H[0, :].reshape(averaged_slices.shape[1:])

    mip = image_data.max(axis=0)
    pred = nmf_model.transform([mip.reshape(-1)])
    bg = pred[0][0] * background_component

    # Step 6: The signal is obtained as the difference between the image block and the background component
    # This will require reshaping and broadcasting the background_component to match the original image_data shape
    signal = image_data.max(axis=0) - bg

    save_image(out_dir / img_path.with_suffix('.tiff').name, bg.astype(np.uint16))
    save_image(out_dir / img_path.with_suffix('.tif').name, signal.astype(np.uint16))


if __name__ == '__main__':
    from multiprocessing import Pool
    from tqdm import tqdm
    out_dir.mkdir(exist_ok=True)
    files = sorted(crop_path.glob('*.v3dpbd'))

    # main((r"C:\Users\zzh\Downloads\0011.tiff", 12, 1))

    with Pool(6) as p:
        for res in tqdm(p.imap(main, files), total=len(files)): pass