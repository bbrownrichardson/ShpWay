from shp_way.read_shp import ShapefileGraph
from shp_way.spatial_grid import SpatialGrid
from shapely.geometry import Point
from scipy import spatial


class CollisionDetection:
    """
    Class represents a collision detection object. Object determines entry points of all visitation objects using
    collision detection.

    Public Attributes
    ------------------
    - num_rows: number of rows used in spatial grid used for collision detection. Users can provide a set value or have
    value auto-generated. Value will be auto-generated by default.
    - num_cols: number of columns used in spatial grid used for collision detection. Users can provide a set value or
    have value auto-generated. Value will be auto-generated by default.

    'Private' Attributes
    ------------------
    - grid: SpatialGrid object
    - shp_graph: ShapefileGraph object
    """
    def __init__(self, read_obj, rows=None, cols=None):
        """
        Parameters
        ----------
        read_obj: ReadShapefiles
            a ReadShapefiles object containing the shapefiles
        rows: int, optional
            number of rows to be used for grid instead of auto-generating the value
        cols: int, optional
            number of rows to be used for grid instead of auto-generating the value
        """
        self.grid = None
        self.shp_graph = None

        if (isinstance(rows, int) and rows > 1) and (isinstance(cols, int) and cols > 1):
            self.__num_rows = rows
            self.__num_cols = cols
        else:
            self.__num_rows = None
            self.__num_cols = None

        self.__create_grid(read_obj)
        self.__scan()

    def num_rows(self):
        """
        :return: generated num of rows used for the spatial grid
        """
        return self.__num_rows

    def num_cols(self):
        """
        :return: generated num of columns used for the spatial grid
        """
        return self.__num_cols

    def __create_grid(self, read_obj):
        """
        Creates the spatial grid to partition the collision detection process
        :param read_obj: ReadShapefile object
        :return: None
        """
        self.shp_graph = ShapefileGraph(read_obj)

        self.grid = SpatialGrid(self.shp_graph.bb_max, self.shp_graph.bb_min,
                                self.shp_graph.polygon_heights, self.shp_graph.polygon_widths,
                                num_rows=self.__num_rows, num_cols=self.__num_cols)
        self.__num_rows = self.grid.num_rows
        self.__num_cols = self.grid.num_cols

    def __scan(self):
        """
        Initialize collision detection process
        :return:
        """
        self.__scan_nodes_to_cells()
        self.__scan_visitation_objects()

    def __scan_nodes_to_cells(self):
        """
        Determine which cell partitions each node falls upon
        :return: None
        """
        bbox_max = self.grid.absolute_max
        bbox_min = self.grid.absolute_min

        for node in self.shp_graph.graph.nodes:
            if isinstance(node, tuple):
                x = node[0]
                y = node[1]

                col_cell = int((((x - bbox_min[0]) / (bbox_max[0] - bbox_min[0])) * self.__num_cols))
                row_cell = int((((y - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.__num_rows))
                self.grid.grid[row_cell][col_cell].append((float(node[0]), float(node[1])))

    def __scan_visitation_objects(self):
        """
        Initialize process to scanning for each visitation objects
        :return: None
        """
        for building, directory in self.shp_graph.reference_directory.items():
            self.__scan_visitation_objects_to_cells(directory)
            self.__assign_entry_points(directory)

    def __scan_visitation_objects_to_cells(self, directory):
        """
        Determine which cell partitions a visitation object falls upon using the objects' individual
        reference directory
        :param directory: hash table data structure containing needed information relating each object
        :return: None
        """
        polygon = directory['shp_reference']
        bbox_max = self.grid.absolute_max
        bbox_min = self.grid.absolute_min

        min_xy = (polygon.bounds[0], polygon.bounds[1])
        max_xy = (polygon.bounds[2], polygon.bounds[3])

        min_cell = (int((((min_xy[0] - bbox_min[0])/(bbox_max[0] - bbox_min[0])) * self.__num_cols)),
                    int((((min_xy[1] - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.__num_rows)))

        max_cell = (int((((max_xy[0] - bbox_min[0])/(bbox_max[0] - bbox_min[0])) * self.__num_cols)),
                    int((((max_xy[1] - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.__num_rows)))

        for i in range(min_cell[0], max_cell[0] + 1, 1):
            for j in range(min_cell[1], max_cell[1] + 1, 1):
                directory['assigned_cell_partitions'].append((j, i))

    def __assign_entry_points(self, directory):
        """
        Assign entry points for all visitation objects using references of nodes
        :param directory: hash table data structure containing needed information relating each object
        :return: None
        """
        polygon = directory['shp_reference']
        count = 0

        for cell in directory['assigned_cell_partitions']:
            x = cell[0]
            y = cell[1]

            if len(self.grid.grid[x][y]) != 0:
                for node in self.grid.grid[x][y]:
                    node_pt = Point((float(node[0]), float(node[1])))

                    if node_pt.intersects(polygon) and (float(node[0]), float(node[1])) not in \
                            directory['entry_nodes']:
                        count += 1
                        directory['entry_nodes'].append((float(node[0]), float(node[1])))

        if count == 0:
            found_nodes = list()

            mx = max(directory['assigned_cell_partitions'])
            mx_x = mx[0]
            mx_y = mx[1]

            mn = min(directory['assigned_cell_partitions'])
            mn_x = mn[0]
            mn_y = mn[1]

            node = self.shp_graph.midpoint(polygon.bounds[0], polygon.bounds[1], polygon.bounds[2], polygon.bounds[3])

            while len(found_nodes) == 0 and mx_x <= len(self.grid.grid) and mx_y < len(self.grid.grid) \
                    and mn_y >= 0 and mx_x >= 0:

                for r in range(mn_y, mx_y, 1):
                    for c in range(mn_x, mx_x, 1):
                        if len(self.grid.grid[c][r]) != 0:
                            found_nodes.extend(self.grid.grid[c][r])

                if mx_x < len(self.grid.grid):
                    mx_x += 1
                if mx_y < len(self.grid.grid):
                    mx_y += 1
                if mn_x > 0:
                    mn_x -= 1
                if mn_y > 0:
                    mn_y -= 1

            if len(found_nodes) == 0:
                found_nodes = self.shp_graph.graph.nodes

            tree = spatial.KDTree(found_nodes)
            tree.query([node])
            output = tree.query([node])
            directory['entry_nodes'].append(list(found_nodes).__getitem__(output[1][0]))
