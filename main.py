from shapefile_navigator import ShapefileNavigator


def main():
    pathways = "shapefile_navigator/shapefiles/roads.shp"
    visitation = "shapefile_navigator/shapefiles/buildings.shp"
    sn = ShapefileNavigator(pathways, visitation)
    sn.show_path('Taylor Hall', 'Lowry Student Center')


if __name__ == '__main__':
    main()
