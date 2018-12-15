from read_shp import ProcessShapeFiles
from bounding_boxes import BoundingBoxTracker
from shapely.geometry import box, Point


class CollisionDetection:
    def __init__(self, read_obj, num_rows=2, num_cols=2):
        self.bbox_obj = None
        self.cells = None
        self.bboxes = None

        self.num_rows = num_rows
        self.num_cols = num_cols

        self.buildings_sf = read_obj.buildings_sf
        self.pathways_sf = read_obj.pathways_sf
        self.build_process = ProcessShapeFiles()
        self.create_field(self.num_rows, self.num_cols)
        self.scan()

    def create_field(self, rows, cols):
        self.build_process.process(self.buildings_sf)
        self.build_process.process(self.pathways_sf)

        self.bbox_obj = BoundingBoxTracker(self.build_process.bb_max, self.build_process.bb_min)
        # TODO: FIGURE OUT HOW TO DETERMINE NUMBER OF BOUNDING BOXES
        # self.bbox_obj.create_bounding_boxes(rows, cols)
        # return self.bbox_obj.get_bboxes()

        self.bbox_obj.create_bbox_grid(rows, cols)
        self.cells = self.bbox_obj.grid
        self.bbox_obj.create_bounding_boxes(rows, cols)
        self.bboxes = self.bbox_obj.bounding_boxes

    def scan(self):
        self.scan_nodes_to_cell()
        self.scan_building_to_cell()

    def scan_nodes_to_cell(self):
        bbox_max = self.bbox_obj.get_absolute_max()
        bbox_min = self.bbox_obj.get_absolute_min()
        for node in self.build_process.graph.nodes:
            if isinstance(node, tuple):
                # node_pt = Point((float(node[0]), float(node[1])))
                # for bbox in self.bboxes:
                #     bbox_poly = box(bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
                #     if node_pt.intersects(bbox_poly):
                #         self.bboxes[bbox].append((float(node[0]), float(node[1])))
                x = node[0]
                y = node[1]

                x_cell = int((((x - bbox_min[0]) / (bbox_max[0] - bbox_min[0])) * self.num_cols))
                y_cell = int((((y - bbox_min[1]) / (bbox_max[1] - bbox_min[1])) * self.num_rows))

                self.cells[x_cell][y_cell].append((float(node[0]), float(node[1])))

    def scan_building_to_cell(self):
        for building, directory in self.build_process.building_directory.items():
            # print(building)
            # print(directory['building_bbox_dir'])
            # print(directory['building_shp_reference'])
            # print(directory['building_entry_nodes'])

            self.assign_cell_to_building(directory['building_shp_reference'], directory)
            # for bbox in self.bboxes:
            #     bbox_poly = box(bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
            #     if polygon.intersects(bbox_poly):
            #         directory['building_bbox_dir'].append(bbox)
            self.scan_building_entry_points(directory)

    def assign_cell_to_building(self, polygon, directory):
        bbox_max = self.bbox_obj.get_absolute_max()
        bbox_min = self.bbox_obj.get_absolute_min()

        min_xy = (polygon.bounds[0], polygon.bounds[1])
        max_xy = (polygon.bounds[2], polygon.bounds[3])
        min_x_max_y = (polygon.bounds[0], polygon.bounds[3])
        max_x_min_y = (polygon.bounds[2], polygon.bounds[1])

        pts = [min_xy, max_xy, min_x_max_y, max_x_min_y]

        for pt in pts:
            x = pt[0]
            y = pt[1]

            x_cell = int((((x - bbox_min[0])/(bbox_max[0] - bbox_min[0])) * self.num_cols))
            y_cell = int((((y - bbox_min[1])/(bbox_max[1] - bbox_min[1])) * self.num_rows))

            directory['building_bbox_dir'].append((x_cell, y_cell))

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
            directory['building_entry_nodes'].append(closest_node)

