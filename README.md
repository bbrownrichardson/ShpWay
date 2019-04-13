# ShpWay: A Shapefile Navigator

ShpWay is a simple Python library that converts shapefiles into a navigation system by the conversion of shapefiles to graph.


## Getting Started

### Requirements

* Python 2.7+
* Two shapefiles
    - a shapefile containing _**polyline**_ shapes to outline the pathways
    - a shapefile containing all potential visitation objects _**polygon shapes is currently only supported**_

### Installation

ShpWay can be installed with pip:

```
$ pip install shp-way
```

or directly from the source code:

```
$ git clone https://github.com/bbrownrichardson/ShpWay.git
$ cd ShpWay
$ python setup.py install
```

#### NOTE:
Some users might experience issues with installing ShpWay due to its Shapely dependency.
To solve this issue simply install Shapely prior to installing ShpWay.

Shapely can be installed either by the following command:
```
pip install Shapely
```

or for Windows the wheels package can be downloaded [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)
- select the appropriate package for your system

After the package is downloaded, cd to the directory containing the wheels package and install using the following command:

```
pip install Shapely-1.6.4.post1-cp37-cp37m-win32.whl
```

**"Shapely-1.6.4.post1-cp37-cp37m-win32.whl" should be replaced with the appropriate package version downloaded**


### Basic Usage
The usage of the library's interface is simple.

```python
from shp_way.shapefile_navigator import ShapefileNavigator

pathways = "shapefiles/roads.shp"
visitation = "shapefiles/buildings.shp"

sn = ShapefileNavigator(pathways, visitation)
```

ShpWay allows users to have control of efficiency in terms of determining spatial grid size. Users can provide a fixed value for the number of rows and columns used in the conversion process. See documentation for more information.

```python
from shp_way.shapefile_navigator import ShapefileNavigator

pathways = "shapefiles/roads.shp"
visitation = "shapefiles/buildings.shp"

sn = ShapefileNavigator(pathways, visitation, rows=15, cols=30)
```

The `sn` object can then be used as described in the `ShpWay-ShapefileNavigator` docs [link here]
