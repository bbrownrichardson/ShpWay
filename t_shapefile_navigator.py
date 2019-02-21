from helper_modules.read_shp import ReadShapeFiles
from helper_modules import path_finder
from helper_modules.collision_detection import CollisionDetection
import networkx as nx
import matplotlib.pyplot as plt
import mplleaflet


class ShapefileNavigator:
    def __init__(self, show_entry_points=False, show_bounding_box=False, show_graph_network=False):
        self._show_entry_points = show_entry_points
        self._show_bounding_box = show_bounding_box
        self._show_graph_network = show_graph_network
        self._selection_map = dict()
        self._start_node = None
        self._destination_node = None
        self._collision_obj = None

        self.building_dir = input("Enter the directory path of the building shapefile:\n")
        self.path_dir = input("\nEnter the directory path of the pathway shapefile:\n")

        self.setup_spatial_partitioning()
        self.start()

    def setup_spatial_partitioning(self):
        if self.path_dir.strip() is '' or self.building_dir.strip() is '':
            self._collision_obj = CollisionDetection(ReadShapeFiles())
        else:
            self._collision_obj = CollisionDetection(ReadShapeFiles(pathways=self.path_dir,
                                                                    destinations=self.building_dir))

    def start(self):
        while True:
            self.build_selection_map(self._collision_obj.build_graph.reference_directory)
            self.select_buildings()
            self.show_graph(self._collision_obj.build_graph.graph, show_entry_points=self._show_entry_points,
                            show_bounding_box=self._show_bounding_box, show_graph_network=self._show_graph_network)

    def build_selection_map(self, buildings):
        for i, building in enumerate(buildings):
            self._selection_map[i] = building

    def select_buildings(self):
        for index, building in sorted(self._selection_map.items()):
            print(str(index) + ": " + str(building))

        try:
            print("\n\nSelect a number to represent the starting building:")
            selection = int(input())
            self._start_node = self._selection_map[selection]
            print("You selected " + str(self._start_node))
            print("\n\nSelect a number to represent the destination building:")
            selection = int(input())
            self._destination_node = self._selection_map[selection]
            print("You selected " + str(self._destination_node) + "\n\n")
        except KeyError:
            print("Please use select a valid key\n\n")
            self.select_buildings()
        except ValueError:
            print("EXITING...")
            return

    def show_graph(self, graph, show_graph_network=False, show_entry_points=False, show_bounding_box=False):
        path = path_finder.nx_shortest_path(graph, self._collision_obj.build_graph.reference_directory[self._start_node],
                                            self._collision_obj.build_graph.reference_directory[self._destination_node])
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
            src_entrance = self._collision_obj.build_graph.reference_directory[self._start_node]
            dst_entrance = self._collision_obj.build_graph.reference_directory[self._destination_node]
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
            for bbox in self._collision_obj.bboxes:
                x.append(bbox[0][0])
                y.append(bbox[0][1])
                x.append(bbox[1][0])
                y.append(bbox[1][1])

            plt.scatter(x=x, y=y)

        mplleaflet.show()


ShapefileNavigator(show_entry_points=True)
