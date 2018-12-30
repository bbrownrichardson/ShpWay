from read_shp import ProcessShapeFiles
from bounding_boxes import BoundingBoxTracker
from shapely.geometry import box, Point
from scipy import spatial


class CollisionDetection:
    def __init__(self, read_obj, rows=None, cols=None):
        self.bbox_obj = None
        self.cells = None
        self.bboxes = None

        if rows is not None and cols is not None:
            self.num_rows = rows
            self.num_cols = cols
        else:
            self.num_rows = None
            self.num_cols = None

        self.buildings_sf = read_obj.buildings_sf
        self.pathways_sf = read_obj.pathways_sf

        self.build_process = ProcessShapeFiles()
        self.create_field(rows=self.num_rows, cols=self.num_cols)
        self.scan()

    def create_field(self, rows=None, cols=None):
        self.build_process.process(self.buildings_sf)
        self.build_process.process(self.pathways_sf)

        self.bbox_obj = BoundingBoxTracker(self.build_process.bb_max, self.build_process.bb_min,
                                           self.build_process.polygon_heights, self.build_process.polygon_widths,
                                           num_rows=rows, num_cols=cols)
        self.cells = self.bbox_obj.grid
        self.bboxes = self.bbox_obj.bounding_boxes
        self.num_rows = self.bbox_obj.num_rows
        self.num_cols = self.bbox_obj.num_cols

    def scan(self):
        self.scan_nodes_to_cell()
        self.scan_building_to_cell()

    def scan_nodes_to_cell(self):
        bbox_max = self.bbox_obj.absolute_max
        bbox_min = self.bbox_obj.absolute_min

        for node in self.build_process.graph.nodes:
            if isinstance(node, tuple):
                x = node[0]
                y = node[1]

                col_cell = int((((x - bbox_min[0]) / (bbox_max[0] - bbox_min[0])) * self.num_cols))
                row_cell = int((((y - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.num_rows))
                self.cells[row_cell][col_cell].append((float(node[0]), float(node[1])))

    def scan_building_to_cell(self):
        for building, directory in self.build_process.building_directory.items():
            # print(building)
            # print(directory['building_bbox_dir'])
            # print(directory['building_shp_reference'])
            # print(directory['building_entry_nodes'])

            self.assign_cells_to_building(directory['building_shp_reference'], directory)
            self.scan_building_entry_points(directory)

    def assign_cells_to_building(self, polygon, directory):
        bbox_max = self.bbox_obj.absolute_max
        bbox_min = self.bbox_obj.absolute_min

        min_xy = (polygon.bounds[0], polygon.bounds[1])
        max_xy = (polygon.bounds[2], polygon.bounds[3])

        min_cell = (int((((min_xy[0] - bbox_min[0])/(bbox_max[0] - bbox_min[0])) * self.num_cols)),
                    int((((min_xy[1] - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.num_rows)))

        max_cell = (int((((max_xy[0] - bbox_min[0])/(bbox_max[0] - bbox_min[0])) * self.num_cols)),
                    int((((max_xy[1] - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.num_rows)))

        for i in range(min_cell[0], max_cell[0] + 1, 1):
            for j in range(min_cell[1], max_cell[1] + 1, 1):
                directory['building_bbox_dir'].append((j, i))

    def scan_building_entry_points(self, directory):
        polygon = directory['building_shp_reference']
        closest_node = None
        shortest_distance = None
        count = 0

        for cell in directory['building_bbox_dir']:
            x = cell[0]
            y = cell[1]

            if len(self.cells[x][y]) != 0:
                if closest_node is None:
                    closest_node = (float(self.cells[x][y][0][0]), float(self.cells[x][y][0][1]))
                    shortest_distance = polygon.exterior.distance(Point(closest_node))
                for node in self.cells[x][y]:
                    node_pt = Point((float(node[0]), float(node[1])))
                    temp_dist = polygon.exterior.distance(node_pt)

                    if node_pt.intersects(polygon) and (float(node[0]), float(node[1])) not in \
                            directory['building_entry_nodes']:
                        count += 1
                        directory['building_entry_nodes'].append((float(node[0]), float(node[1])))
                    if temp_dist < shortest_distance:
                        closest_node = (float(node[0]), float(node[1]))
                        shortest_distance = temp_dist
        if count == 0:
            # directory['building_entry_nodes'].append(closest_node)
            node = self.build_process.midpoint(polygon.bounds[0], polygon.bounds[1], polygon.bounds[2], polygon.bounds[3])
            nodes = self.build_process.graph.nodes
            tree = spatial.KDTree(nodes)
            tree.query([node])
            output = tree.query([node])
            directory['building_entry_nodes'].append(list(self.build_process.graph.nodes).__getitem__(output[1][0]))

