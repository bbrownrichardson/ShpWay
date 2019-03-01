from shp_way.shapefile_navigator import ShapefileNavigator


def main():
    pathways = "shapefiles/roads.shp"
    visitation = "shapefiles/buildings.shp"
    # pathways = r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database" \
    #            r"\Manhattan - NY\shape\roads"
    # visitation = r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database" \
    #              r"\Manhattan - NY\shape\buildings"

    sn = ShapefileNavigator(pathways, visitation)
    # sn.show_directory()

    sn.show_path('Taylor Hall', 'Lowry Student Center')
    # sn.show_path('The Octagon', 'Jane B Aron Residence Hall')
    # sn.show_path('The Octagon', 'The Octagon')
    # sn.show_path('Jane B Aron Residence Hall', 'Jane B Aron Residence Hall')


if __name__ == '__main__':
    main()
