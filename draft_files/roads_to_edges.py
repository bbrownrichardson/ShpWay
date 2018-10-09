import networkx as nx
from shapely.geometry import LineString
import mplleaflet


# for i in sf_1.iterShapes():
#     print(i.points)


# line1 = LineString([(0, 0), (1, 0), (1, 1)])
# line2 = LineString([(0, 1), (1, 1)])
#
# print(line1.intersection(line2))

graph = nx.read_shp("shapefiles/roads.shp")
# print(len(graph.nodes()))
# print(graph.edges())

g = nx.Graph()

for i in graph.nodes():
    g.add_node(i, pos=i)

for i in graph.edges():
    g.add_edge(i[0], i[1])

pos = nx.get_node_attributes(g, 'pos')
nx.draw(g, pos, node_size=10)
mplleaflet.show()
