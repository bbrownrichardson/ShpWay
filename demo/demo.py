import demo_helper as dh


def main():
    # Uncomment with appropriate file path to rebuild navigation systems of desired shapefiles
    # pathways = 'shapefiles/UCR/shape/roads'
    # visitation = 'shapefiles/UCR/shape/buildings'
    # dh.build_navigation_object(pathways, visitation)

    navigation_objects = [('Navigation_System_Pickles/wooster.gpickle',
                           'Navigation_System_Pickles/wooster_ref_dir.gpickle', 'The College of Wooster'),
                          ('Navigation_System_Pickles/denison.gpickle',
                           'Navigation_System_Pickles/denison_ref_dir.gpickle', 'Denison University'),
                          ('Navigation_System_Pickles/riverside.gpickle',
                           'Navigation_System_Pickles/riverside_ref_dir.gpickle', 'University of California Riverside'),
                          ('Navigation_System_Pickles/manhattan.gpickle',
                           'Navigation_System_Pickles/manhattan_ref_dir.gpickle', 'Manhattan New York'),
                          ]

    for obj in navigation_objects:
        print('\n', obj[2])
        print("\n\nEnter 'exit' or enter key to exit this current cycle of the program\n")
        dh.read_navigation_object(obj[0], obj[1])


if __name__ == '__main__':
    main()

