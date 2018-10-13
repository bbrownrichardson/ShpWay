import networkx as nx


def nx_shortest_path(graph, src, dst):
    path = None
    path_length = None
    for src_entrance in src['building_entry_nodes']:
        for dst_entrance in dst['building_entry_nodes']:
            if path is None and path_length is None:
                path = nx.dijkstra_path(graph, source=src_entrance, target=dst_entrance)
                path_length = nx.dijkstra_path_length(graph, source=src_entrance,
                                                      target=dst_entrance)
            else:
                temp_length = nx.dijkstra_path_length(graph, source=src_entrance,
                                                      target=dst_entrance)
                if temp_length < path_length:
                    path = nx.dijkstra_path(graph, source=src_entrance, target=dst_entrance)
                    path_length = temp_length

    return path
