from distutils.core import setup

setup(
    name='ShapefileNavigator',
    version='0.1dev',
    packages=['shapefile_navigator',],
    license='MIT',
    long_description=open('README.md').read(),
    url='https://github.com/bbrownrichardson/Shapefile-Network-Navigator',
    author='Brianna Brown Richardson',
    author_email='bbrownrichardson@gmail.com',
    requires=['pyshp', 'shapely', 'matplotlib', 'networkx', 'scipy']
)