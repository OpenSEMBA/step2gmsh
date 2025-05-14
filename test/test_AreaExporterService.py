from typing import List
import unittest
import os
import numpy as np
import gmsh
from src.mesher import Mesher
from src.AreaExporterService import AreaExporterService
class testAreaExporterService(unittest.TestCase):
    @staticmethod
    def sumAreasFromList(areas:List[float]):
        total:float = 0
        for area in areas:
            total += area
        return total

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

        internalElements = []
        for geometry in geometries:
            if geometry['geometry'] == "Conductor_0":
                totalArea = geometry['area']
            else:
                internalElements.append(geometry['area'])
        areaElements = self.sumAreasFromList(internalElements)

        self.assertAlmostEqual(totalArea, areaElements)
