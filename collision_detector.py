from read_shp import ProcessShapeFiles
from bounding_boxes import BoundingBoxTracker
from shapely.geometry import box, Point


class CollisionDetection:
    def __init__(self, read_obj):
        self.read_obj = read_obj
        self.buildings_sf = read_obj.buildings_sf
        self.pathways_sf = read_obj.pathways_sf
        self.build_process = ProcessShapeFiles()
        self.bboxes = self.create_field()
        self.scan()

    def create_field(self):
        self.build_process.process(self.buildings_sf)
        self.build_process.process(self.pathways_sf)

        b = BoundingBoxTracker(self.build_process.bb_max, self.build_process.bb_min)
        # TODO: FIGURE OUT HOW TO DETERMINE NUMBER OF BOUNDING BOXES
        b.create_bounding_boxes(2, 2)
        return b.get_bboxes()

    def scan(self):
        self.scan_nodes_to_bbox()
        self.scan_building_to_bbox()

    def scan_nodes_to_bbox(self):
        for node in self.build_process.graph.nodes:
            if isinstance(node, tuple):
                node_pt = Point((float(node[0]), float(node[1])))
                for bbox in self.bboxes:
                    bbox_poly = box(bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
                    if node_pt.intersects(bbox_poly):
                        self.bboxes[bbox].append((float(node[0]), float(node[1])))

    def scan_building_to_bbox(self):
        for building, directory in self.build_process.building_directory.items():
            # print(building)
            # print(directory['building_bbox_dir'])
            # print(directory['building_shp_reference'])
            # print(directory['building_entry_nodes'])

            polygon = directory['building_shp_reference']
            for bbox in self.bboxes:
                bbox_poly = box(bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1])
                if polygon.intersects(bbox_poly):
                    directory['building_bbox_dir'].append(bbox)
            self.scan_building_entry_points(directory)

    def scan_building_entry_points(self, directory):
        polygon = directory['building_shp_reference']
        for bbox in directory['building_bbox_dir']:
            for node in self.bboxes[bbox]:
                node_pt = Point((float(node[0]), float(node[1])))
                if node_pt.intersects(polygon):
                    directory['building_entry_nodes'].append((float(node[0]), float(node[1])))

