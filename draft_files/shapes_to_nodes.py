import networkx as nx
import matplotlib.pyplot as plt
from read_shp import *
import mplleaflet


G = nx.Graph()
sf_1 = read_files("shapefiles/buildings.shp", "shapefiles/buildings.dbf")
get_plt_2d(sf_1)
records = list(sf_1.iterRecords())

for i in range(len(sf_1.shapes())):
    pos = node_position(sf_1, i)
    name = records[i][1]
    G.add_node(name, pos=pos)

print(G.nodes)

pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, node_size=10)
nx.draw_networkx_labels(G, pos, font_size=5, font_family='sans-serif')
# plt.axis('off')
# plt.hold(True)
# plt.show()
mplleaflet.show()
