MDATA_BIN_FILE_NAME = "mdata.bin"  # name of binary metadata file
MDATA_BIN_FILE_VERSION = 2  # version of binary metadata file
MC_MDATA_BIN_FILE_NAME = "cmap.bin"  # name of binary metadata file for multichannel volumes
FORMAT_MDATA_FILE_NAME = ".iim.format"  # name of format metadata file
CHANNEL_PREFIX = "CH_"  # prefix identifying a folder containing data of a certain channel
TIME_FRAME_PREFIX = "T_"  # prefix identifying a folder containing data of a certain time frame
DEF_IMG_DEPTH = 8  # default image depth
NUL_IMG_DEPTH = 0  # invalid image depth
NATIVE_RTYPE = 0  # loadVolume returns the same bytes per channel as in the input image
DEF_IMG_FORMAT = "tif"  # default image format
STATIC_STRINGS_SIZE = 1024  # size of static C-strings
RAW_FORMAT = "Vaa3D raw"  # unique ID for the RawVolume class
SIMPLE_RAW_FORMAT = "Vaa3D raw (series, 2D)"  # unique ID for the SimpleVolumeRaw class
STACKED_RAW_FORMAT = "Vaa3D raw (tiled, 2D)"  # unique ID for the StackedVolume class
TILED_FORMAT = "Vaa3D raw (tiled, 3D)"  # unique ID for the TiledVolume class
TILED_MC_FORMAT = "Vaa3D raw (tiled, 4D)"  # unique ID for the TiledMCVolume class
TIF3D_FORMAT = "TIFF (3D)"  # unique ID for multipage TIFF format (nontiled)
SIMPLE_FORMAT = "TIFF (series, 2D)"  # unique ID for the SimpleVolume class
STACKED_FORMAT = "TIFF (tiled, 2D)"  # unique ID for the StackedVolume class
TILED_TIF3D_FORMAT = "TIFF (tiled, 3D)"  # unique ID for multipage TIFF format (tiled)
TILED_MC_TIF3D_FORMAT = "TIFF (tiled, 4D)"  # unique ID for multipage TIFF format (nontiled, 4D)
UNST_TIF3D_FORMAT = "TIFF (unstitched, 3D)"  # unique ID for multipage TIFF format (nontiled, 4D)
BDV_HDF5_FORMAT = "HDF5 (BigDataViewer)"  # unique ID for BDV HDF5
IMS_HDF5_FORMAT = "HDF5 (Imaris IMS)"  # unique ID for IMS HDF5
MAPPED_FORMAT = "Mapped Volume"  # unique ID for mapped volumes
MULTISLICE_FORMAT = "MultiSlice Volume"  # unique ID for multi-slice volumes
MULTICYCLE_FORMAT = "MultiCycle Volume"  # unique ID for multi-cycle volumes
VOLATILE_FORMAT = "Volatile Volume"  # unique ID for volatile volumes
TIME_SERIES = "Time series"  # unique ID for the TimeSeries classes


class Rect:
    def __init__(self, h0, v0, h1, v1):
        self.H0 = h0
        self.H1 = h1
        self.V0 = v0
        self.V1 = v1
