from read_shp import read_files, node_position, get_plt_2d
import networkx as nx
from shapely.geometry import Point, mapping, LineString
from shapely.geometry.polygon import Polygon
from collections import defaultdict
import mplleaflet
import matplotlib.pyplot as plt


sf = read_files("shapefiles/buildings.shp", "shapefiles/buildings.dbf")
# get_plt_2d(sf)
sf_2 = read_files("shapefiles/roads.shp", "shapefiles/roads.dbf")
graph = nx.Graph()

records = list(sf.iterRecords())

shape_name_dir = dict()
buildings_entrances = defaultdict(list)

for i in range(len(sf.shapes())):
    pos = node_position(sf, i)
    name = records[i][1]
    shape_name_dir[name] = Polygon(sf.shape(i).points)
    graph.add_node(name, pos=pos)

building = shape_name_dir['Kauke Hall']
# for i in sf_2.shapes():
#     line = LineString(i.points)
#
#     if line.touches(building):
#         buildings_entrances['Kauke Hall'].append(line.intersection(building))

for i in sf_2.shapes():
    prev_point = None
    counter = 0
    for point in i.points:
        graph.add_node(point, pos=point)
        if counter > 0:
            graph.add_edge(prev_point, point)
        prev_point = point
        counter += 1

# coors_obj = buildings_entrances['Kauke Hall']
# for i in coors_obj:
#     print(mapping(i)['coordinates'])

# print(len(shape_name_dir))
# print(len(sf_2.shapes()))

pos = nx.get_node_attributes(graph, 'pos')
nx.draw(graph, pos, node_size=10)
nx.draw_networkx_labels(graph, pos, font_size=5, font_family='sans-serif')
mplleaflet.show()
