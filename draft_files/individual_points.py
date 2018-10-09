from read_shp import read_files
import networkx as nx
import mplleaflet


sf = read_files("shapefiles/roads.shp", "shapefiles/roads.dbf")
print(len(sf.shapes()))

graph = nx.Graph()

for i in sf.shapes():
    prev_point = None
    counter = 0
    for point in i.points:
        graph.add_node(point, pos=point)
        if counter > 0:
            graph.add_edge(prev_point, point)
        prev_point = point
        counter += 1

print(len(graph.nodes))
pos = nx.get_node_attributes(graph, 'pos')
nx.draw(graph, pos, node_size=10)

mplleaflet.show()
