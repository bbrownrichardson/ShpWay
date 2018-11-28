from collision_detector import CollisionDetection
from read_shp import ReadShapeFiles
from path_finder import nx_shortest_path
import time
import matplotlib.pyplot as plt
import xlsxwriter


x = list()
y = list()
x_dij = list()
y_dij = list()
x_bell = list()
y_bell = list()
x_as = list()
y_as = list()

workbook = xlsxwriter.Workbook('TimeComplexity.xlsx')
time_size = workbook.add_worksheet(name='time and grid size')
dij_size = workbook.add_worksheet(name='Dijkstra')
bell = workbook.add_worksheet(name='Ford Bellman')
astar = workbook.add_worksheet(name='A-star')

denison_buildings = r'C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database\Denison\shape\buildings.shp'
denison_pathways = r'C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database\Denison\shape\roads.shp'

time_list = list()
dij_list = list()
bell_list = list()
astar_list = list()
for i in range(2, 100, 1):
    start = time.time()
    collision_obj = CollisionDetection(ReadShapeFiles(), num_rows=i, num_cols=i)
    end = time.time()
    duration = end - start
    print(str(i) + ": Collision Detection took " + str(duration) + "\n")
    x.append(i * i)
    y.append(duration)
    time_list.append([i*i, duration])

    # COW
    taylor = collision_obj.build_process.building_directory['Taylor Hall']
    lowry = collision_obj.build_process.building_directory['Lowry Student Center']

    # DENISON
    # taylor = collision_obj.build_process.building_directory['Shaw Hall']
    # lowry = collision_obj.build_process.building_directory['Higley Hall']

    start = time.time()
    nx_shortest_path(collision_obj.build_process.graph, taylor, lowry)
    end = time.time()
    duration = end - start
    print(str(i) + ": Dijkstra took " + str(duration) + "\n")
    x_dij.append(i * i)
    y_dij.append(duration)
    dij_list.append([i*i, duration])

    start = time.time()
    nx_shortest_path(collision_obj.build_process.graph, taylor, lowry, alg_name='bellman_ford_path')
    end = time.time()
    duration = end - start
    print(str(i) + ": Bellman Ford took " + str(duration) + "\n")
    x_bell.append(i * i)
    y_bell.append(duration)
    bell_list.append([i*i, duration])

    start = time.time()
    nx_shortest_path(collision_obj.build_process.graph, taylor, lowry, alg_name='astar_path')
    end = time.time()
    duration = end - start
    print(str(i) + ": A* took " + str(duration) + "\n")
    x_as.append(i * i)
    y_as.append(duration)
    astar_list.append([i*i, duration])


# plt.plot(x, y)
# # plt.plot(x_dij, y_dij, color='green')
# # plt.plot(x_bell, y_bell, color='red')
# # plt.plot(x_as, y_as, color='yellow')
# plt.show()

# Iterate over the data and write it out row by row.
worksheets = [(time_list, time_size), (dij_list, dij_size), (bell_list, bell), (astar_list, astar)]

for worksheet in worksheets:
    row = 0
    col = 0
    for size, dur in (worksheet[0]):
        worksheet[1].write(row, col,     size)
        worksheet[1].write(row, col + 1, dur)
        row += 1

# Write a total using a formula.
# worksheet.write(row, 0, 'Total')
# worksheet.write(row, 1, '=SUM(B1:B4)')

workbook.close()
