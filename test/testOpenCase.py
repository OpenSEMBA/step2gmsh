from typing import Dict

from test.utils import assertListOfFloatsAlmostEqual
import gmsh
import unittest
from src.OpenCase import OpenMultiwire, BoundingBox

class testOpenCase(unittest.TestCase):
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
        boundingBox = OpenMultiwire._getBoundingBox((1,circleSurface))


        assertListOfFloatsAlmostEqual(tuple(boundingBox.edges.values()), tuple(expectedBoundingBoxEdges.values()))

    def testCanGetBoundingBoxFromListOfSurfaces(self):
        pass
        
