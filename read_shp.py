import matplotlib.pyplot as plt
import mplleaflet
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
    def __init__(self, pathways="shapefiles/roads.shp", buildings="shapefiles/buildings.shp"):
        self.pathways_sf = self.read_files(pathways)
        self.buildings_sf = self.read_files(buildings)

    @staticmethod
    def read_files(file_path):
        """
        Apply shapefile reader to main and dBASE files
        :param file_path: main file selected
        :return: reference to reader of selected files
        """
        sf = shapefile.Reader(file_path)
        # sf = shapefile.Reader(shp=open(shp_file, "rb"), dbf=open(dbf_file, "rb"))
        return sf


class ProcessShapeFiles:
    def __init__(self):
        self.bb_max = None
        self.bb_mx_x = None
        self.bb_mx_y = None

        self.bb_min = None
        self.bb_mn_x = None
        self.bb_mn_y = None

        self.polygon_widths = list()
        self.polygon_heights = list()

        self.graph = nx.Graph()
        self.building_directory = dict()

    def process(self, sf):
        if sf.shapes()[0].shapeType == POLYGON:
            self.process_polygons(sf)
        elif sf.shapes()[0].shapeType == POLYLINE:
            self.process_polylines(sf)

    def process_polygons(self, sf):
        records = list(sf.iterRecords())
        for i, shape in enumerate(sf.shapes()):
            # TODO: TURN OFF LATER
            self.draw_polygons(shape)
            self.calculate_polygon_size(shape.bbox)

            # pos = self.node_position(sf, i)
            name = records[i][1]
            # self.graph.add_node(name, pos=pos)

            self.building_directory[name] = {
                'building_bbox_dir': list(),
                'building_shp_reference':  Polygon(shape.points),
                'building_entry_nodes': list()
            }

            if self.bb_mx_x is None and self.bb_mx_y is None and self.bb_mn_x is None and self.bb_mn_y is None:
                self.bb_mn_x = shape.bbox[0]
                self.bb_mn_y = shape.bbox[1]
                self.bb_mx_x = shape.bbox[2]
                self.bb_mx_y = shape.bbox[3]

            else:
                if self.bb_mn_x > shape.bbox[0]:
                    self.bb_mn_x = shape.bbox[0]
                if self.bb_mn_y > shape.bbox[1]:
                    self.bb_mn_y = shape.bbox[1]
                if self.bb_mx_x < shape.bbox[2]:
                    self.bb_mx_x = shape.bbox[2]
                if self.bb_mx_y < shape.bbox[3]:
                    self.bb_mx_y = shape.bbox[3]

        self.bb_max = (self.bb_mx_x, self.bb_mx_y)
        self.bb_min = (self.bb_mn_x, self.bb_mn_y)

    def calculate_polygon_size(self, bbox):
        mn_x = bbox[0]
        mn_y = bbox[1]
        mx_x = bbox[2]
        mx_y = bbox[3]

        mn = (mn_x, mn_y)
        mn_x_mx_y = (mx_x, mn_y)
        mx = (mx_x, mx_y)

        width = self.distance_calculation(mn, mn_x_mx_y)
        height = self.distance_calculation(mn_x_mx_y, mx)

        self.polygon_widths.append(width)
        self.polygon_heights.append(height)

    def process_polylines(self, sf):
        for shape in sf.shapes():
            # self.pathways_reference.append(LineString(shape.points))
            prev_point = None
            counter = 0

            if self.bb_mx_x is None and self.bb_mx_y is None and self.bb_mn_x is None and self.bb_mn_y is None:
                self.bb_mn_x = shape.bbox[0]
                self.bb_mn_y = shape.bbox[1]
                self.bb_mx_x = shape.bbox[2]
                self.bb_mx_y = shape.bbox[3]
            else:
                if self.bb_mn_x > shape.bbox[0]:
                    self.bb_mn_x = shape.bbox[0]
                if self.bb_mn_y > shape.bbox[1]:
                    self.bb_mn_y = shape.bbox[1]
                if self.bb_mx_x < shape.bbox[2]:
                    self.bb_mx_x = shape.bbox[2]
                if self.bb_mx_y < shape.bbox[3]:
                    self.bb_mx_y = shape.bbox[3]

            for point in shape.points:
                self.graph.add_node(point, pos=point)
                if counter > 0:
                    self.graph.add_edge(prev_point, point, weight=self.distance_calculation(prev_point, point))
                prev_point = point
                counter += 1

        self.bb_max = (self.bb_mx_x, self.bb_mx_y)
        self.bb_min = (self.bb_mn_x, self.bb_mn_y)

    @staticmethod
    def draw_polygons(shape):
        x = [j[0] for j in shape.points[:]]
        y = [j[1] for j in shape.points[:]]
        plt.plot(x, y)

    def get_graph(self):
        pos = nx.get_node_attributes(self.graph, 'pos')
        nx.draw(self.graph, pos, node_size=10)

        mplleaflet.show()

    def node_position(self, sf_reader, index):
        bbox = sf_reader.shape(index).bbox
        mid = self.midpoint(bbox[0], bbox[1], bbox[2], bbox[3])
        return mid

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
