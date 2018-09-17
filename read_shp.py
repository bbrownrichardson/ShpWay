import matplotlib.pyplot as plt
import shapefile


def read_files(shp_file, dbf_file):
    """
    Apply shapefile reader to main and dBASE files
    :param shp_file: main file selected
    :param dbf_file: dBASE file selected
    :return: reference to reader of selected files
    """
    sf = shapefile.Reader(shp=open(shp_file, "rb"), dbf=open(dbf_file, "rb"))
    return sf


def node_position(sf_reader, index):
    bbox = sf_reader.shape(index).bbox
    mid = midpoint(bbox[0], bbox[1], bbox[2], bbox[3])
    return mid


def midpoint(x1, y1, x2, y2):
    coord = ((x1 + x2)/2, (y1 + y2)/2)
    return coord


def get_plt_2d(sf):
    """
    Get the matplotlib figure that contains the 2D scene of selected
    shapefile
    :return: ax - figure containing visualized data
    """
    for shape in sf.shapes():
        x = [j[0] for j in shape.points[:]]
        y = [j[1] for j in shape.points[:]]
        plt.plot(x, y)
