import gmsh
import os
from src.mesher import Mesher
from src.ShapesClassification import ShapesClassification
import sys

sys.path.insert(0, '.')

dirPath = os.path.dirname(os.path.realpath(__file__)) + '/'
testdataPath = dirPath + '/../testData/'

def countEntitiesInPhysicalGroupWithName(name: str):
    return len(
        gmsh.model.getEntitiesForPhysicalGroup(
            *Mesher.getPhysicalGroupWithName(name)
        )
    )

def inputFileFromCaseName(caseName):
    return testdataPath + caseName + '/' + caseName + ".step"

def testGetNumberFromEntityName():
    assert (ShapesClassification.getNumberFromName(
        'Shapes/Conductor_1',
        'Conductor_') == 1
    )

    assert (ShapesClassification.getNumberFromName(
        'Shapes/solid_wire_002/Conductor_002/Conductor_002',
        'Conductor_') == 2
    )

def testPartiallyFilledCoax():
    Mesher.runCase(testdataPath, 'partially_filled_coax')

def testEmptyCoax():
    Mesher.runCase(testdataPath, 'empty_coax')

def testTwoWiresCoax():
    Mesher.runCase(testdataPath, 'two_wires_coax')

def testTwoWiresOpen():
    Mesher.runCase(testdataPath, 'two_wires_open')

def testFiveWires():
    Mesher.runCase(testdataPath, 'five_wires')

def testThreeWiresRibbon():
    Mesher.runCase(testdataPath, 'three_wires_ribbon')

def testNestedCoax():
    Mesher.runCase(testdataPath, 'nested_coax')

def testAgrawal1981():
    Mesher.runCase(testdataPath, 'agrawal1981')

def testMeshFromStepWithPartiallyFilledCoax():
    gmsh.initialize()
    
    caseName = 'partially_filled_coax'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)

    pGs = gmsh.model.getPhysicalGroups()
    assert (len(pGs) == 4)

    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Dielectric_1' in pGNames)
    assert ('Vacuum' in pGNames)

    c0pG = Mesher.getPhysicalGroupWithName('Conductor_0')
    c0ents = gmsh.model.getEntitiesForPhysicalGroup(*c0pG)
    assert (len(c0ents) == 1)

    gmsh.finalize()

def testEmptyCoax():
    Mesher.runStepToGmsh(testdataPath, 'empty_coax')

def testEmptyCoaxMeshFromStep():
    gmsh.initialize()

    caseName = 'empty_coax'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)

    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 3)
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Vacuum' in pGNames)

    gmsh.finalize()

def testTwoWiresCoax():
    Mesher.runStepToGmsh(testdataPath, 'two_wires_coax')

def testTwoWiresOpen():
    Mesher.runStepToGmsh(testdataPath, 'two_wires_open')

def testTwoWiresCoaxMeshFromStep():
    gmsh.initialize()

    caseName = 'two_wires_coax'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)

    pGs = gmsh.model.getPhysicalGroups()
    assert (len(pGs) == 4)

    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Vacuum' in pGNames)

    c0pG = Mesher.getPhysicalGroupWithName('Conductor_0')
    c0ents = gmsh.model.getEntitiesForPhysicalGroup(*c0pG)
    assert (len(c0ents) == 1)

    gmsh.finalize()

def testMeshFromStepWithTwoWiresCoaxNew():
    gmsh.initialize()

    caseName = 'two_wires_coax'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)
    
    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 4)
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Vacuum' in pGNames)

    assert (countEntitiesInPhysicalGroupWithName('Conductor_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_2') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Vacuum') == 1)

    gmsh.finalize()

def testMeshFromStepWithTwoWiresOpenNew():
    gmsh.initialize()

    caseName = 'two_wires_open'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)
    
    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 4)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Vacuum' in pGNames)
    assert ('OpenRegion_0' in pGNames)

    assert (countEntitiesInPhysicalGroupWithName('Conductor_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_2') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Vacuum') == 1)
    assert (countEntitiesInPhysicalGroupWithName('OpenRegion_0') == 1)

    gmsh.finalize()

def testMeshFromStepWithFiveWires():
    gmsh.initialize()

    caseName = 'five_wires'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)
    
    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 12)
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Conductor_3' in pGNames)
    assert ('Conductor_4' in pGNames)
    assert ('Conductor_5' in pGNames)
    assert ('Dielectric_1' in pGNames)
    assert ('Dielectric_2' in pGNames)
    assert ('Dielectric_3' in pGNames)
    assert ('Dielectric_4' in pGNames)
    assert ('Dielectric_5' in pGNames)
    assert ('Vacuum' in pGNames)

    assert (countEntitiesInPhysicalGroupWithName('Conductor_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_2') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_3') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_4') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_5') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Dielectric_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_2') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_3') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_4') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_5') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Vacuum') == 1)

    gmsh.finalize()

def testMeshFromStepWithThreeWiresRibbon():
    gmsh.initialize()

    caseName = 'three_wires_ribbon'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)
    
    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 8)
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Dielectric_0' in pGNames)
    assert ('Dielectric_1' in pGNames)
    assert ('Dielectric_2' in pGNames)
    assert ('Vacuum' in pGNames)
    assert ('OpenRegion_0' in pGNames)

    assert (countEntitiesInPhysicalGroupWithName('Conductor_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_2') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Dielectric_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_2') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Vacuum') == 1)
    assert (countEntitiesInPhysicalGroupWithName('OpenRegion_0') == 1)

    gmsh.finalize()

def testMeshFromStepWithNestedCoax():
    gmsh.initialize()

    caseName = 'nested_coax'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)
    
    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 4)
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Vacuum' in pGNames)

    assert (countEntitiesInPhysicalGroupWithName('Conductor_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_1') == 2)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_2') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Vacuum') == 2)

    gmsh.finalize()

def testMeshFromStepWithAgrawal1981():
    gmsh.initialize()

    caseName = 'agrawal1981'
    Mesher.meshFromStep(inputFileFromCaseName(caseName), caseName)
    
    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 9)
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Conductor_3' in pGNames)
    assert ('Dielectric_1' in pGNames)
    assert ('Dielectric_2' in pGNames)
    assert ('Dielectric_3' in pGNames)
    assert ('Vacuum' in pGNames)
    assert ('OpenRegion_0' in pGNames)

    assert (countEntitiesInPhysicalGroupWithName('Conductor_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_2') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_3') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Dielectric_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_2') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_3') == 1)

    assert (countEntitiesInPhysicalGroupWithName('Vacuum') == 2)
    assert (countEntitiesInPhysicalGroupWithName('OpenRegion_0') == 1)

    gmsh.finalize()

def testAgrawal1981MeshFromStep():
    gmsh.initialize()

    Mesher.meshFromStep(testdataPath, 'agrawal1981')

    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Conductor_3' in pGNames)
    assert ('OpenRegion_0' in pGNames)
    assert ('Dielectric_1' in pGNames)
    assert ('Dielectric_2' in pGNames)
    assert ('Dielectric_3' in pGNames)
    assert ('Vacuum' in pGNames)

    assert (countEntitiesInPhysicalGroupWithName('Conductor_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_2') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Conductor_3') == 1)
    assert (countEntitiesInPhysicalGroupWithName('OpenRegion_0') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_1') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_2') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Dielectric_3') == 1)
    assert (countEntitiesInPhysicalGroupWithName('Vacuum') == 2)

    gmsh.finalize()

def testPartiallyFilledCoaxStepShapes():
    caseName = 'partially_filled_coax'

    gmsh.initialize()
    gmsh.model.add(caseName)
    stepShapes = ShapesClassification(
        gmsh.model.occ.importShapes(
            testdataPath + caseName + '/' + caseName + '.step'
        )
    )

    gmsh.finalize()

    assert (len(stepShapes.pecs) == 2)
    assert (len(stepShapes.dielectrics) == 1)

def testFiveWiresStepShapes():
    caseName = 'five_wires'

    gmsh.initialize()
    gmsh.model.add(caseName)
    stepShapes = ShapesClassification(
        gmsh.model.occ.importShapes(
            testdataPath + caseName + '/' + caseName + '.step'
        )
    )

    gmsh.finalize()

    assert (len(stepShapes.pecs) == 6)
    assert (len(stepShapes.dielectrics) == 5)

def testThreeWiresRibbonStepShapes():
    caseName = 'three_wires_ribbon'

    gmsh.initialize()
    gmsh.model.add(caseName)
    stepShapes = ShapesClassification(
        gmsh.model.occ.importShapes(
            testdataPath + caseName + '/' + caseName + '.step'
        )
    )

    gmsh.finalize()

    assert (len(stepShapes.open) == 1)
    assert (len(stepShapes.pecs) == 3)
    assert (len(stepShapes.dielectrics) == 3)
