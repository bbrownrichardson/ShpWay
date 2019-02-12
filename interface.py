import read_shp
import collision_detection
import path_finder


class Navigator:
    def __init__(self, pathway_shapefile, visitation_shapefile, rows=None, cols=None):
        self.r = read_shp.ReadShapeFiles(pathways=pathway_shapefile, destinations=visitation_shapefile)
        self.collision_obj = collision_detection.CollisionDetection(self.r, rows=rows, cols=cols)

    def get_graph(self):
        pass

    def get_visitation_directory(self):
        pass

    def find_path(self, src, dst):
        pass



