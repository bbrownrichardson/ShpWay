import shapefile
import networkx as nx
from shapely.geometry import Polygon
import math

NULL = 0
POINT = 1
POLYLINE = 3
POLYGON = 5
MULTIPOINT = 8
POINTZ = 11
POLYLINEZ = 13
POLYGONZ = 15
MULTIPOINTZ = 18
POINTM = 21
POLYLINEM = 23
POLYGONM = 25
MULTIPOINTM = 28
MULTIPATCH = 31


class ReadShapeFiles:
    def __init__(self, pathways="shapefiles/roads.shp", visitation_points="shapefiles/buildings.shp"):

        self.__pathways_sf = None
        self.__buildings_sf = None
        self.__integrity_check(pathways, visitation_points)

    @property
    def pathways_sf(self):
        return self.__pathways_sf

    @property
    def buildings_sf(self):
        return self.__buildings_sf

    def __integrity_check(self, pathways, buildings):
        pathways_sf = self.__read_files(pathways)
        buildings_sf = self.__read_files(buildings)
        if pathways_sf.shape(0).shapeType == POLYLINE and buildings_sf.shape(0).shapeType == POLYGON:
            self.__pathways_sf = pathways_sf
            self.__buildings_sf = buildings_sf
        elif pathways_sf.shape(0).shapeType == POLYGON and buildings_sf.shape(0).shapeType == POLYLINE:
            self.__pathways_sf = buildings_sf
            self.__buildings_sf = pathways_sf
        else:
            raise ValueError("The included shapefiles are not supported")

    @staticmethod
    def __read_files(file_path):
        """
        Apply shapefile reader to main file
        :param file_path: main file selected
        :return: reference to reader of selected files
        """
        sf = shapefile.Reader(file_path)
        # sf = shapefile.Reader(shp=open(shp_file, "rb"), dbf=open(dbf_file, "rb"))
        return sf


class ProcessShapeFiles:
    def __init__(self):
        self.__bb_max = None
        self.__bb_mx_x = None
        self.__bb_mx_y = None

        self.__bb_min = None
        self.__bb_mn_x = None
        self.__bb_mn_y = None

        self.__polygon_widths = list()
        self.__polygon_heights = list()

        self.__graph = nx.Graph()
        self.__building_directory = dict()

    @property
    def bb_max(self):
        return self.__bb_max

    @property
    def bb_min(self):
        return self.__bb_min

    @property
    def polygon_widths(self):
        return self.__polygon_widths

    @property
    def polygon_heights(self):
        return self.__polygon_heights

    @property
    def graph(self):
        return self.__graph

    @property
    def building_directory(self):
        return self.__building_directory

    def process(self, sf):
        if sf.shapes()[0].shapeType == POLYGON:
            self.__process_polygons(sf)
        elif sf.shapes()[0].shapeType == POLYLINE:
            self.__process_polylines(sf)

    def __process_polygons(self, sf):
        records = list(sf.iterRecords())
        for i, shape in enumerate(sf.shapes()):
            self.__calculate_polygon_size(shape.bbox)
            name = records[i][1]

            self.__building_directory[name] = {
                'building_bbox_dir': list(),
                'building_shp_reference':  Polygon(shape.points),
                'building_entry_nodes': list()
            }

            if self.__bb_mx_x is None and self.__bb_mx_y is None and self.__bb_mn_x is None and self.__bb_mn_y is None:
                self.__bb_mn_x = shape.bbox[0]
                self.__bb_mn_y = shape.bbox[1]
                self.__bb_mx_x = shape.bbox[2]
                self.__bb_mx_y = shape.bbox[3]

            else:
                if self.__bb_mn_x > shape.bbox[0]:
                    self.__bb_mn_x = shape.bbox[0]
                if self.__bb_mn_y > shape.bbox[1]:
                    self.__bb_mn_y = shape.bbox[1]
                if self.__bb_mx_x < shape.bbox[2]:
                    self.__bb_mx_x = shape.bbox[2]
                if self.__bb_mx_y < shape.bbox[3]:
                    self.__bb_mx_y = shape.bbox[3]

        self.__bb_max = (self.__bb_mx_x, self.__bb_mx_y)
        self.__bb_min = (self.__bb_mn_x, self.__bb_mn_y)

    def __calculate_polygon_size(self, bbox):
        mn_x = bbox[0]
        mn_y = bbox[1]
        mx_x = bbox[2]
        mx_y = bbox[3]

        mn = (mn_x, mn_y)
        mn_x_mx_y = (mx_x, mn_y)
        mx = (mx_x, mx_y)

        width = self.distance_calculation(mn, mn_x_mx_y)
        height = self.distance_calculation(mn_x_mx_y, mx)

        self.__polygon_widths.append(width)
        self.__polygon_heights.append(height)

    def __process_polylines(self, sf):
        for shape in sf.shapes():
            prev_point = None
            counter = 0

            if self.__bb_mx_x is None and self.__bb_mx_y is None and self.__bb_mn_x is None and self.__bb_mn_y is None:
                self.__bb_mn_x = shape.bbox[0], self.__bb_mn_y = shape.bbox[1]
                self.__bb_mx_x = shape.bbox[2], self.__bb_mx_y = shape.bbox[3]
            else:
                if self.__bb_mn_x > shape.bbox[0]:
                    self.__bb_mn_x = shape.bbox[0]
                if self.__bb_mn_y > shape.bbox[1]:
                    self.__bb_mn_y = shape.bbox[1]
                if self.__bb_mx_x < shape.bbox[2]:
                    self.__bb_mx_x = shape.bbox[2]
                if self.__bb_mx_y < shape.bbox[3]:
                    self.__bb_mx_y = shape.bbox[3]

            for point in shape.points:
                self.__graph.add_node(point, pos=point)
                if counter > 0:
                    self.__graph.add_edge(prev_point, point, weight=self.distance_calculation(prev_point, point))
                prev_point = point
                counter += 1

        self.__bb_max = (self.__bb_mx_x, self.__bb_mx_y)
        self.__bb_min = (self.__bb_mn_x, self.__bb_mn_y)

    @staticmethod
    def midpoint(x1, y1, x2, y2):
        coord = ((x1 + x2)/2, (y1 + y2)/2)
        return coord

    @staticmethod
    def distance_calculation(coord1, coord2):
        x1 = coord1[0]
        y1 = coord1[1]
        x2 = coord2[0]
        y2 = coord2[1]
        return math.hypot(x2 - x1, y2 - y1)
