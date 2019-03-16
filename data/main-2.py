from shp_way.shapefile_navigator import ShapefileNavigator
import time
import xlsxwriter


def main():
    shapefiles_v_p = [[r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\The College of Wooster\shape\roads",
                       r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\The College of Wooster\shape\buildings"],
                      [r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\Denison\shape\roads",
                       r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\Denison\shape\buildings"],
                      [r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\UCR\shape\roads",
                       r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\UCR\shape\buildings"],
                      [r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\Manhattan - NY\shape\roads",
                       r"C:\Users\rbrib\OneDrive\Documents\College\The College of Wooster\Senior\I.S\GIS Database"
                       r"\Manhattan - NY\shape\buildings"]
                      ]

    file_names = ["College of Wooster", "Denison University", "UCR", "Manhattan"]
    workbook = xlsxwriter.Workbook('TimeComplexity.xlsx')

    for j, file_pair in enumerate(shapefiles_v_p):
        print("Processing...", file_names[j])
        p = file_pair[0]
        v = file_pair[1]

        start = time.time()
        sn = ShapefileNavigator(p, v)
        end = time.time()
        duration = end - start

        print("{} took {} seconds".format(file_names[j], duration))
        print("Rows and cols:", sn.get_rows_cols())


if __name__ == '__main__':
    main()
