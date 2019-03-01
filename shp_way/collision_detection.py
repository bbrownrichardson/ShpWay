from shp_way.read_shp import ShapefileGraph
from shp_way.spatial_grid import SpatialGrid
from shapely.geometry import Point
from scipy import spatial


class CollisionDetection:
    def __init__(self, read_obj, rows=None, cols=None, create_bboxes=False):
        self.grid_obj = None
        self.bboxes = None
        self.build_graph = None

        if (isinstance(rows, int) and rows > 1) and (isinstance(cols, int) and cols > 1):
            self.__num_rows = rows
            self.__num_cols = cols
        else:
            self.__num_rows = None
            self.__num_cols = None

        self.__create_field(read_obj, create_bboxes)
        self.__scan()

    def __create_field(self, read_obj, create_bboxes):
        self.build_graph = ShapefileGraph(read_obj)

        self.grid_obj = SpatialGrid(self.build_graph.bb_max, self.build_graph.bb_min,
                                    self.build_graph.polygon_heights, self.build_graph.polygon_widths,
                                    num_rows=self.__num_rows, num_cols=self.__num_cols, create_bboxes=create_bboxes)
        self.bboxes = self.grid_obj.bounding_boxes
        self.__num_rows = self.grid_obj.num_rows
        self.__num_cols = self.grid_obj.num_cols

    def __scan(self):
        self.__scan_nodes_to_cell()
        self.__scan_building_to_cell()

    def __scan_nodes_to_cell(self):
        bbox_max = self.grid_obj.absolute_max
        bbox_min = self.grid_obj.absolute_min

        for node in self.build_graph.graph.nodes:
            if isinstance(node, tuple):
                x = node[0]
                y = node[1]

                col_cell = int((((x - bbox_min[0]) / (bbox_max[0] - bbox_min[0])) * self.__num_cols))
                row_cell = int((((y - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.__num_rows))
                self.grid_obj.grid[row_cell][col_cell].append((float(node[0]), float(node[1])))

    def __scan_building_to_cell(self):
        for building, directory in self.build_graph.reference_directory.items():
            # print(building)
            # print(directory['building_bbox_dir'])
            # print(directory['building_shp_reference'])
            # print(directory['building_entry_nodes'])

            self.__assign_cells_to_building(directory['building_shp_reference'], directory)
            self.__scan_building_entry_points(directory)

    def __assign_cells_to_building(self, polygon, directory):
        bbox_max = self.grid_obj.absolute_max
        bbox_min = self.grid_obj.absolute_min

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

            if len(self.grid_obj.grid[x][y]) != 0:
                for node in self.grid_obj.grid[x][y]:
                    node_pt = Point((float(node[0]), float(node[1])))

                    if node_pt.intersects(polygon) and (float(node[0]), float(node[1])) not in \
                            directory['building_entry_nodes']:
                        count += 1
                        directory['building_entry_nodes'].append((float(node[0]), float(node[1])))

        if count == 0:
            found_nodes = list()

            mx = max(directory['building_bbox_dir'])
            mx_x = mx[0]
            mx_y = mx[1]

            mn = min(directory['building_bbox_dir'])
            mn_x = mn[0]
            mn_y = mn[1]

            node = self.build_graph.midpoint(polygon.bounds[0], polygon.bounds[1], polygon.bounds[2], polygon.bounds[3])

            # TODO: Think about how to proceed in the opposite direction if max OR min cells are approached
            # TODO: rest of the cellular search should not suffer because max OR min has been hit
            while len(found_nodes) == 0 and mx_x <= len(self.grid_obj.grid) and mx_y < len(self.grid_obj.grid) \
                    and mn_y >= 0 and mx_x >= 0:

                for r in range(mn_y, mx_y, 1):
                    for c in range(mn_x, mx_x, 1):
                        if len(self.grid_obj.grid[c][r]) != 0:
                            found_nodes.extend(self.grid_obj.grid[c][r])

                if mx_x < len(self.grid_obj.grid):
                    mx_x += 1
                if mx_y < len(self.grid_obj.grid):
                    mx_y += 1
                if mn_x > 0:
                    mn_x -= 1
                if mn_y > 0:
                    mn_y -= 1

            if len(found_nodes) == 0:
                found_nodes = self.build_graph.graph.nodes

            tree = spatial.KDTree(found_nodes)
            tree.query([node])
            output = tree.query([node])
            directory['building_entry_nodes'].append(list(found_nodes).__getitem__(output[1][0]))
