from shp_way import collision_detection, path_finder, read_shp
import matplotlib.pyplot as plt
import mplleaflet
import random


class ShapefileNavigator:
    def __init__(self, pathway_shapefile, visitation_shapefile, rows=None, cols=None):
        self.__r_obj = read_shp.ReadShapeFiles(pathways=pathway_shapefile, destinations=visitation_shapefile)
        self.__collision_obj = collision_detection.CollisionDetection(self.__r_obj, rows=rows, cols=cols)

    def get_rows_cols(self):
        return self.__collision_obj.num_rows(), self.__collision_obj.num_cols()

    def get_graph(self):
        return self.__collision_obj.build_graph.graph

    def get_reference_directory(self):
        return self.__collision_obj.build_graph.reference_directory

    def show_directory(self):
        directory = self.get_reference_directory()
        for i in directory.keys():
            print(i)

    @staticmethod
    def get_algorithms():
        return path_finder.ShortestPathAlgorithm

    def find_path(self, src, dst, algorithm=path_finder.ShortestPathAlgorithm.dijkstra):
        directory = self.get_reference_directory()
        if directory.get(src) is None or directory.get(dst) is None:
            raise read_shp.ShapeFileNavigatorException("src or dst is not present in reference directory")
        path = path_finder.nx_shortest_path(self.get_graph(), directory[src], directory[dst], alg_name=algorithm)
        return path

    def show_path(self, src, dst, show_graph=False, show_entry_points=True):
        path = self.find_path(src, dst)
        if path is None:
            raise read_shp.ShapeFileNavigatorException("path does not exist")

        if show_graph:
            color = 'blue'
            line_width = 5
        else:
            color = (random.uniform(0, .5), random.uniform(0, .5), random.uniform(0, .5))
            line_width = 2

        x = list()
        y = list()
        for i in path:
            x.append(i[0])
            y.append(i[1])

        plt.plot(x, y, color=color, linestyle='solid', marker='o', linewidth=line_width)

        if show_graph is True:
            graph = self.get_graph()
            pos = path_finder.nx.get_node_attributes(graph, 'pos')
            path_finder.nx.draw(graph, pos, node_size=10)
            path_finder.nx.draw_networkx_labels(graph, pos, font_size=5, font_family='sans-serif')

        if show_entry_points is True:
            x_coordinates = [path[0][0], path[-1][0]]
            y_coordinates = [path[0][1], path[-1][1]]
            plt.scatter(x=x_coordinates, y=y_coordinates, color=color, marker='D')

        mplleaflet.show()
