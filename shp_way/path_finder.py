import networkx as nx
import enum


class ShortestPathAlgorithm(enum.Enum):
    dijkstra = 1
    a_star = 2
    bellman_ford = 3


def nx_shortest_path(graph, src, dst, alg_name=ShortestPathAlgorithm.dijkstra):
    try:
        if alg_name.value == 1:
            return __nx_dijkstra(graph, src, dst)
        elif alg_name.value == 2:
            return __nx_astar(graph, src, dst)
        elif alg_name.value == 3:
            return __nx_bellman(graph, src, dst)
    except nx.NetworkXNoPath:
        return None


def __nx_dijkstra(graph, src, dst):
    path = None
    path_length = None

    for src_entrance in src['building_entry_nodes']:
        for dst_entrance in dst['building_entry_nodes']:
            if path is None and path_length is None:

                path = nx.dijkstra_path(graph, source=src_entrance, target=dst_entrance)
                path_length = nx.dijkstra_path_length(graph, source=src_entrance, target=dst_entrance)
            else:
                temp_length = nx.dijkstra_path_length(graph, source=src_entrance, target=dst_entrance)
                if temp_length < path_length:
                    path = nx.dijkstra_path(graph, source=src_entrance, target=dst_entrance)
                    path_length = temp_length

    return path


def __nx_astar(graph, src, dst):
    path = None
    path_length = None

    for src_entrance in src['building_entry_nodes']:
        for dst_entrance in dst['building_entry_nodes']:
            if path is None and path_length is None:

                path = nx.astar_path(graph, source=src_entrance, target=dst_entrance)
                path_length = nx.astar_path_length(graph, source=src_entrance, target=dst_entrance)
            else:
                temp_length = nx.astar_path_length(graph, source=src_entrance, target=dst_entrance)
                if temp_length < path_length:
                    path = nx.astar_path(graph, source=src_entrance, target=dst_entrance)
                    path_length = temp_length

    return path


def __nx_bellman(graph, src, dst):
    path = None
    path_length = None

    for src_entrance in src['building_entry_nodes']:
        for dst_entrance in dst['building_entry_nodes']:
            if path is None and path_length is None:

                path = nx.bellman_ford_path(graph, source=src_entrance, target=dst_entrance)
                path_length = nx.bellman_ford_path_length(graph, source=src_entrance, target=dst_entrance)
            else:
                temp_length = nx.bellman_ford_path_length(graph, source=src_entrance, target=dst_entrance)
                if temp_length < path_length:
                    path = nx.bellman_ford_path(graph, source=src_entrance, target=dst_entrance)
                    path_length = temp_length

    return path

