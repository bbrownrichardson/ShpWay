from read_shp import ReadShapeFiles
import path_finder
from collision_detector import CollisionDetection
import networkx as nx
import matplotlib.pyplot as plt
import mplleaflet


class ShapefileNavigator:
    def __init__(self):
        self.building_dir = input("Enter the directory path of the building shapefile:\n")
        self.path_dir = input("\nEnter the directory path of the pathway shapefile:\n")
        self.selection_map = dict()
        self.start_node = None
        self.destination_node = None
        self.collision_obj = None
        self.setup_spatial_partitioning()
        self.start()

    def setup_spatial_partitioning(self):
        if self.path_dir.strip() is '' or self.building_dir.strip() is '':
            self.collision_obj = CollisionDetection(ReadShapeFiles())
        else:
            self.collision_obj = CollisionDetection(ReadShapeFiles(pathways=self.path_dir, buildings=self.building_dir))

    def start(self):
        while True:
            self.build_selection_map(self.collision_obj.build_process.building_directory)
            self.select_buildings()
            self.show_graph(self.collision_obj.build_process.graph, show_entry_points=True, show_bounding_box=False,
                            show_graph_network=True)

    def build_selection_map(self, buildings):
        for i, building in enumerate(buildings):
            self.selection_map[i] = building

    def select_buildings(self):
        for index, building in self.selection_map.items():
            print(str(index) + ": " + str(building))

        print("\n\nSelect a number to represent the starting building:")
        selection = int(input())
        self.start_node = self.selection_map[selection]
        print("You selected " + str(self.start_node))

        print("\n\nSelect a number to represent the destination building:")
        selection = int(input())
        self.destination_node = self.selection_map[selection]
        print("You selected " + str(self.destination_node) + "\n\n")

    def show_graph(self, graph, show_graph_network=False, show_entry_points=False, show_bounding_box=False):
        path = path_finder.nx_shortest_path(graph, self.collision_obj.build_process.building_directory[self.start_node],
                                            self.collision_obj.build_process.building_directory[self.destination_node])
        x = list()
        y = list()
        for i in path:
            x.append(i[0])
            y.append(i[1])

        plt.plot(x, y, color='blue', linestyle='solid', marker='o', markerfacecolor='blue', markersize=10)

        if show_graph_network is True:
            pos = nx.get_node_attributes(graph, 'pos')
            nx.draw(graph, pos, node_size=10)
            nx.draw_networkx_labels(graph, pos, font_size=5, font_family='sans-serif')

        if show_entry_points is True:
            src_entrance = self.collision_obj.build_process.building_directory[self.start_node]
            dst_entrance = self.collision_obj.build_process.building_directory[self.destination_node]
            x = list()
            y = list()

            for node in src_entrance['building_entry_nodes']:
                x.append(node[0])
                y.append(node[1])

            for node in dst_entrance['building_entry_nodes']:
                x.append(node[0])
                y.append(node[1])

            plt.scatter(x=x, y=y)

        if show_bounding_box is True:
            x = list()
            y = list()
            for bbox in self.collision_obj.bboxes:
                x.append(bbox[0][0])
                y.append(bbox[0][1])
                x.append(bbox[1][0])
                y.append(bbox[1][1])

            plt.scatter(x=x, y=y)

        mplleaflet.show()


ShapefileNavigator()
