from collision_detector import CollisionDetection
from read_shp import ReadShapeFiles
from path_finder import nx_shortest_path
import time
import matplotlib.pyplot as plt


x = list()
y = list()
x_dij = list()
y_dij = list()
x_bell = list()
y_bell = list()
x_as = list()
y_as = list()

for i in range(2, 100, 1):
    start = time.time()
    collision_obj = CollisionDetection(ReadShapeFiles(), num_rows=i, num_cols=i)
    end = time.time()
    duration = end - start
    print(str(i) + ": Collision Detection took " + str(duration) + "\n")
    x.append(i * i)
    y.append(duration)

    taylor = collision_obj.build_process.building_directory['Taylor Hall']
    lowry = collision_obj.build_process.building_directory['Lowry Student Center']

    start = time.time()
    nx_shortest_path(collision_obj.build_process.graph, taylor, lowry)
    end = time.time()
    duration = end - start
    print(str(i) + ": Dijkstra took " + str(duration) + "\n")
    x_dij.append(i * i)
    y_dij.append(duration)

    start = time.time()
    nx_shortest_path(collision_obj.build_process.graph, taylor, lowry, alg_name='bellman_ford_path')
    end = time.time()
    duration = end - start
    print(str(i) + ": Bellman Ford took " + str(duration) + "\n")
    x_bell.append(i * i)
    y_bell.append(duration)

    start = time.time()
    nx_shortest_path(collision_obj.build_process.graph, taylor, lowry, alg_name='astar_path')
    end = time.time()
    duration = end - start
    print(str(i) + ": A* took " + str(duration) + "\n")
    x_as.append(i * i)
    y_as.append(duration)


plt.plot(x, y)
plt.plot(x_dij, y_dij)
plt.plot(x_bell, y_bell)
plt.plot(x_as, y_as)
plt.show()
