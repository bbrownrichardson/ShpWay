from read_shp import read_files
import networkx as nx
import mplleaflet
import matplotlib.pyplot as plt
import math


sf = read_files("shapefiles/roads.shp", "shapefiles/roads.dbf")


def distance(x1, x2, y1, y2):
    return math.hypot(x2-x1, y2-y1)


graph = nx.Graph()

for i in sf.shapes():
    prev_point = None
    counter = 0
    for point in i.points:
        graph.add_node(point, pos=point)
        if counter > 0:
            dist = distance(prev_point[0], prev_point[1], point[0], point[1])
            graph.add_edge(prev_point, point, distance=dist)
        prev_point = point
        counter += 1

print(min(graph.nodes))
print(max(graph.nodes))

path = nx.dijkstra_path(graph, source=min(graph.nodes), target=max(graph.nodes))
# path_2 = nx.shortest_path(graph, source=min(graph.nodes), target=max(graph.nodes))

pos = nx.get_node_attributes(graph, 'pos')
nx.draw(graph, pos, node_size=10)
x = list()
y = list()
for i in path:
    x.append(i[0])
    y.append(i[1])
plt.plot(x, y, color='blue', linestyle='solid', marker='o', markerfacecolor='blue', markersize=10)

# x = list()
# y = list()
# for i in path_2:
#     x.append(i[0])
#     y.append(i[1])
#
# plt.plot(x, y, color='green', linestyle='solid', marker='o', markerfacecolor='green', markersize=10)

x = [-81.9439629]
x_2 = [-81.9210558]
y = [40.806506]
y_2 = [40.8138977]

plt.plot(x, y, color='yellow', marker='o', markerfacecolor='yellow', markersize=20)
plt.plot(x_2, y_2, color='yellow', marker='o', markerfacecolor='yellow', markersize=20)

mplleaflet.show()
