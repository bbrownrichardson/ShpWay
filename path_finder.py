import networkx as nx


def nx_shortest_path(graph, src, dst, alg_name='dijkstra_path'):
    algorithm = getattr(nx, alg_name)
    algorithm_length = getattr(nx, alg_name+'_length')
    path = None
    path_length = None

    for src_entrance in src['building_entry_nodes']:
        for dst_entrance in dst['building_entry_nodes']:
            if src_entrance is not None and dst_entrance is not None:
                if path is None and path_length is None:

                    path = algorithm(graph, source=src_entrance, target=dst_entrance)
                    path_length = algorithm_length(graph, source=src_entrance, target=dst_entrance)
                else:
                    temp_length = algorithm_length(graph, source=src_entrance, target=dst_entrance)
                    if temp_length < path_length:
                        path = algorithm(graph, source=src_entrance, target=dst_entrance)
                        path_length = temp_length
    return path
