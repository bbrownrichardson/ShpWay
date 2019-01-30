from read_shp import ProcessShapeFiles
from bounding_boxes import BoundingBoxTracker
from shapely.geometry import Point
from scipy import spatial


class CollisionDetection:
    def __init__(self, read_obj, rows=None, cols=None):
        self.bbox_obj = None
        self.cells = None
        self.bboxes = None

        if isinstance(rows, int) and isinstance(cols, int):
            self.__num_rows = rows
            self.__num_cols = cols
        else:
            self.__num_rows = None
            self.__num_cols = None

        self.buildings_sf = read_obj.buildings_sf
        self.pathways_sf = read_obj.pathways_sf

        self.build_process = ProcessShapeFiles()
        self.__create_field(rows=self.__num_rows, cols=self.__num_cols)
        self.__scan()

    def __create_field(self, rows=None, cols=None):
        self.build_process.process(self.buildings_sf)
        self.build_process.process(self.pathways_sf)

        self.bbox_obj = BoundingBoxTracker(self.build_process.bb_max, self.build_process.bb_min,
                                           self.build_process.polygon_heights, self.build_process.polygon_widths,
                                           num_rows=rows, num_cols=cols)
        self.cells = self.bbox_obj.grid
        self.bboxes = self.bbox_obj.bounding_boxes
        self.__num_rows = self.bbox_obj.num_rows
        self.__num_cols = self.bbox_obj.num_cols

    def __scan(self):
        self.__scan_nodes_to_cell()
        self.__scan_building_to_cell()

    def __scan_nodes_to_cell(self):
        bbox_max = self.bbox_obj.absolute_max
        bbox_min = self.bbox_obj.absolute_min

        for node in self.build_process.graph.nodes:
            if isinstance(node, tuple):
                x = node[0]
                y = node[1]

                col_cell = int((((x - bbox_min[0]) / (bbox_max[0] - bbox_min[0])) * self.__num_cols))
                row_cell = int((((y - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.__num_rows))
                self.cells[row_cell][col_cell].append((float(node[0]), float(node[1])))

    def __scan_building_to_cell(self):
        for building, directory in self.build_process.building_directory.items():
            # print(building)
            # print(directory['building_bbox_dir'])
            # print(directory['building_shp_reference'])
            # print(directory['building_entry_nodes'])

            self.__assign_cells_to_building(directory['building_shp_reference'], directory)
            self.__scan_building_entry_points(directory)

    def __assign_cells_to_building(self, polygon, directory):
        bbox_max = self.bbox_obj.absolute_max
        bbox_min = self.bbox_obj.absolute_min

        min_xy = (polygon.bounds[0], polygon.bounds[1])
        max_xy = (polygon.bounds[2], polygon.bounds[3])

        min_cell = (int((((min_xy[0] - bbox_min[0])/(bbox_max[0] - bbox_min[0])) * self.__num_cols)),
                    int((((min_xy[1] - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.__num_rows)))

        max_cell = (int((((max_xy[0] - bbox_min[0])/(bbox_max[0] - bbox_min[0])) * self.__num_cols)),
                    int((((max_xy[1] - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.__num_rows)))

        for i in range(min_cell[0], max_cell[0] + 1, 1):
            for j in range(min_cell[1], max_cell[1] + 1, 1):
                directory['building_bbox_dir'].append((j, i))

    def __scan_building_entry_points(self, directory):
        polygon = directory['building_shp_reference']
        count = 0

        for cell in directory['building_bbox_dir']:
            x = cell[0]
            y = cell[1]

            if len(self.cells[x][y]) != 0:
                for node in self.cells[x][y]:
                    node_pt = Point((float(node[0]), float(node[1])))

                    if node_pt.intersects(polygon) and (float(node[0]), float(node[1])) not in \
                            directory['building_entry_nodes']:
                        count += 1
                        directory['building_entry_nodes'].append((float(node[0]), float(node[1])))

        if count == 0:
            # directory['building_entry_nodes'].append(closest_node)
            node = self.build_process.midpoint(polygon.bounds[0], polygon.bounds[1], polygon.bounds[2],
                                               polygon.bounds[3])
            nodes = self.build_process.graph.nodes
            tree = spatial.KDTree(nodes)
            tree.query([node])
            output = tree.query([node])
            directory['building_entry_nodes'].append(list(self.build_process.graph.nodes).__getitem__(output[1][0]))
