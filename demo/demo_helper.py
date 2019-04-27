import mplleaflet
import shp_way.path_finder as path_finder
import shp_way.read_shp as read_shp
import random
import matplotlib.pyplot as plt
import pickle
import shp_way.shapefile_navigator as sn
import networkx as nx


def build_navigation_object(pathways, visitation):
    print("BUILDING NAVIGATION SYSTEM")
    x = sn.ShapefileNavigator(pathways, visitation)
    print("NAVIGATION SYSTEM BUILD COMPLETED")
    nx.write_gpickle(x.get_graph(), "graph.gpickle")
    with open("ref_dir.gpickle", 'wb') as f:
        pickle.dump(x.get_reference_directory(), f)


def read_navigation_object(graph_data, reference_dir_data):
    graph = nx.read_gpickle(graph_data)

    with open(reference_dir_data, 'rb') as f:
        reference_dir = pickle.load(f)

    initiate(graph, reference_dir)


def initiate(graph, ref_dir):
    selection_map = build_selection_map(ref_dir)
    select_buildings(graph, ref_dir, selection_map)


def build_selection_map(buildings):
    selection_map = dict()
    for i, building in enumerate(sorted(buildings)):
        selection_map[i] = building
    return selection_map


def select_buildings(graph, ref_dir, selection_map):
    for index, building in sorted(selection_map.items()):
        print(str(index) + ": " + str(building))

    print("\n\nEnter 'exit' or enter key to exit this current cycle of the program\n")

    try:
        print("\n\nSelect a number to represent the starting building:")
        selection = int(input())
        start_node = selection_map[selection]
        print("You selected " + str(start_node))
        print("\n\nSelect a number to represent the destination building:")
        selection = int(input())
        destination_node = selection_map[selection]
        print("You selected " + str(destination_node) + "\n\n")
        show_path(graph, ref_dir, start_node, destination_node)
        select_buildings(graph, ref_dir, selection_map)
    except KeyError:
        print("Please use select a valid key\n\n")
        select_buildings(graph, ref_dir, selection_map)
    except ValueError:
        print("EXITING...")
        return


def find_path(graph, ref_dir, src, dst, algorithm=path_finder.ShortestPathAlgorithm.dijkstra):
    directory = ref_dir
    if directory.get(src) is None or directory.get(dst) is None:
        raise read_shp.ShapeFileNavigatorException("src or dst is not present in reference directory")
    path = path_finder.nx_shortest_path(graph, directory[src]['entry_nodes'],
                                        directory[dst]['entry_nodes'], alg_name=algorithm)
    return path


def show_path(graph, ref_dir, src, dst, algorithm=path_finder.ShortestPathAlgorithm.dijkstra,
              show_graph=False, show_entry_points=True):

    path = find_path(graph, ref_dir, src, dst, algorithm=algorithm)
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
        pos = path_finder.nx.get_node_attributes(graph, 'pos')
        path_finder.nx.draw(graph, pos, node_size=10)
        path_finder.nx.draw_networkx_labels(graph, pos, font_size=5, font_family='sans-serif')

    if show_entry_points is True:
        x_coordinates = [path[0][0], path[-1][0]]
        y_coordinates = [path[0][1], path[-1][1]]
        plt.scatter(x=x_coordinates, y=y_coordinates, color=color, marker='D')

    mplleaflet.show()
