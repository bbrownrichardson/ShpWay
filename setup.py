from distutils.core import setup

setup(
    name='ShpWay: A Shapefile Navigator',
    version='0.1',
    packages=['shp_way', ],
    license='MIT',
    long_description=open('README.md').read(),
    url='https://github.com/bbrownrichardson/ShpWay',
    author='Brianna Brown Richardson',
    author_email='bbrownrichardson@gmail.com',
    requires=['pyshp', 'shapely', 'matplotlib', 'networkx', 'scipy', 'mplleaflet']
)