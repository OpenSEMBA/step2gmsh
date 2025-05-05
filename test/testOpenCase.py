from typing import Dict
from src.mesher import ShapesClassification
from src.utils import assertListOfFloatsAlmostEqual
from src.BoundingBox import BoundingBox
import gmsh
import unittest

class testOpenCase(unittest.TestCase):
    _TEST_MODEL_NAME: str = "Test_Model"
    _DEBUG_MODE = False #Set to true if gmsh ui needed for debug

    def setUp(self):
        self.meshing_options = {
    
            "Mesh.MshFileVersion": 2.2,   # Mandatory for MFEM compatibility
            "Mesh.MeshSizeFromCurvature": 20,
            "Mesh.ElementOrder": 3,
            "Mesh.ScalingFactor": 1e-3,
            "Mesh.SurfaceFaces": 1,
            "Mesh.MeshSizeMax": 20,

            "General.DrawBoundingBoxes": 1,
            "General.Axes": 1,

            "Geometry.SurfaceType": 2,    # Diplay surfaces as solids rather than dashed lines.
            # "Geometry.OCCBoundsUseStl": 1,
            # "Geometry.OCCSewFaces": 1,
            # "Geometry.Tolerance": 1e-3,
        }

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

        assertListOfFloatsAlmostEqual(tuple(boundingBox.edges.values()), tuple(expectedBoundingBoxEdges.values()))
        
    def testCanCreateOpenVacuum(self):
        gmsh.initialize()
        gmsh.model.add(self._TEST_MODEL_NAME)
        allshapes = ShapesClassification(
            gmsh.model.occ.importShapes(
                'testData/unshielded_multiwire/unshielded_multiwire.step', 
                highestDimOnly=False,
                )
        )
        allshapes.buildOpenVacuumDomain()
        gmsh.model.occ.synchronize()
        for [opt, val] in self.meshing_options.items():
            gmsh.option.setNumber(opt, val)
        gmsh.model.mesh.generate(2)
        gmsh.write('testOpen.vtk')
        gmsh.write('testOpen.msh')

    def tearDown(self):
        if self._DEBUG_MODE:
            gmsh.fltk.run()
        gmsh.finalize()