import unittest
import os
import numpy as np
import gmsh
from src.mesher import Mesher
from src.AreaExporterService import AreaExporterService
class testAreaExporterService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dirPath = os.path.dirname(os.path.realpath(__file__)) + '/'
        cls.testdataPath = cls.dirPath + '/../testData/'

    def setUp(self):
        gmsh.initialize()

    def tearDown(self):
        gmsh.finalize()
    def inputFileFromCaseName(self, caseName):
        return self.testdataPath + caseName + '/' + caseName + ".step"

    def testAreaExporterReturnsTrueValues(self):
        caseName = 'five_wires'
        Mesher().meshFromStep(self.inputFileFromCaseName(caseName), caseName)
        areaExporter = AreaExporterService()
        areaExporter.addPhysicalModelOfDimension(dimension=1)
        areaExporter.addPhysicalModelOfDimension(dimension=2)
        geometries = areaExporter.computedAreas['geometries']
        vacuumArea = [x['area'] for x in geometries if x['geometry'] == 'Vacuum_0']
        otherAreas = [x['area'] for x in geometries if x['geometry'] != 'Vacuum_0']
        a=1
