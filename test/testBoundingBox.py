from typing import List, Dict, Tuple
import unittest
import gmsh
from src.BoundingBox import BoundingBox
from src import utils

class testBoundingBox(unittest.TestCase):
    _TEST_MODEL_NAME: str = "Test_Model"

    def testCanDefineBoundingBox(self):
        inputExample = (-1, 2.0, 3, 5, 6, 7)
        expectedBoundingBoxEdges: Dict[str, float] = {
                    'xmin': -1,
                    'ymin': 2.0,
                    'zmin': 3,
                    'xmax': 5,
                    'ymax': 6,
                    'zmax': 7,
                }
        boundingBox = BoundingBox(inputExample)
        self.assertDictEqual(boundingBox.edges, expectedBoundingBoxEdges)

    def testCanGetBoundingBoxFromSurface(self):
        expectedBoundingBoxEdges: Dict[str, float] = {
            'xmin': -10,
            'ymin': -10,
            'zmin': 0,
            'xmax': 10,
            'ymax': 10,
            'zmax': 0,
        }

        gmsh.initialize()
        gmsh.model.add(self._TEST_MODEL_NAME)
        circleSurface = gmsh.model.occ.addCircle(0, 0, 0, 10, tag=1)
        boundingBox = BoundingBox._getBoundingBox((1,circleSurface))

        utils.assertListOfFloatsAlmostEqual(tuple(boundingBox.edges.values()), tuple(expectedBoundingBoxEdges.values()))
    
    def testCanGetBoundingBoxFromListOfSurfaces(self):
        expectedBoundingBoxEdges: Dict[str, float] = {
            'xmin': -10,
            'ymin': -10,
            'zmin': 0,
            'xmax': 35,
            'ymax': 40,
            'zmax': 0,
        }

        gmsh.initialize()
        gmsh.model.add(self._TEST_MODEL_NAME)
        circleSurface = gmsh.model.occ.addCircle(0, 0, 0, 10, tag=1)
        innerCircleSurface = gmsh.model.occ.addCircle(0, 0, 0, 5, tag=2)
        secondCircleSurface = gmsh.model.occ.addCircle(25, 30, 0, 10, tag=3)
        groupOfCircles = [(1, circleSurface), (1, innerCircleSurface), (1, secondCircleSurface)]
        boundingBox = BoundingBox.getBoundingBoxFromGroup(groupOfCircles)

        utils.assertListOfFloatsAlmostEqual(tuple(boundingBox.edges.values()), tuple(expectedBoundingBoxEdges.values()))