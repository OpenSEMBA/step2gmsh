import gmsh
import os
from src.mesher import *
import sys

sys.path.insert(0, '.')


dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
testdata_path = dir_path + '/../testData/'


def countEntitiesInPhysicalGroupWithName(name: str):
    return len(
        gmsh.model.getEntitiesForPhysicalGroup(
            *getPhysicalGrupWithName(name)
        )
    )

def inputFileFromCaseName(case_name):
    return testdata_path + case_name + '/' + case_name + ".step"

def test_getNumberFromEntityName():
    assert (ShapesClassification.getNumberFromName(
        'Shapes/Conductor_1',
        'Conductor_') == 1
    )

    assert (ShapesClassification.getNumberFromName(
        'Shapes/solid_wire_002/Conductor_002/Conductor_002',
        'Conductor_') == 2
    )


def test_partially_filled_coax():
    runCase(testdata_path, 'partially_filled_coax')


def test_meshFromStep_with_partially_filled_coax():
    gmsh.initialize()
    
    case_name = 'partially_filled_coax'
    meshFromStep(inputFileFromCaseName(case_name), case_name)

    pGs = gmsh.model.getPhysicalGroups()
    assert (len(pGs) == 4)

    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Dielectric_1' in pGNames)
    assert ('Vacuum' in pGNames)

    c0pG = getPhysicalGrupWithName('Conductor_0')
    c0ents = gmsh.model.getEntitiesForPhysicalGroup(*c0pG)
    assert (len(c0ents) == 1)

    # gmsh.fltk.run()  # for debugging only.
    gmsh.finalize()


def test_empty_coax():
    runCase(testdata_path, 'empty_coax')


def test_meshFromStep_with_empty_coax():
    gmsh.initialize()

    case_name = 'empty_coax'
    meshFromStep(inputFileFromCaseName(case_name), case_name)

    pGs = gmsh.model.getPhysicalGroups()
    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]

    assert (len(pGs) == 3)
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Vacuum' in pGNames)

    # gmsh.fltk.run()  # for debugging only.
    gmsh.finalize()


def test_two_wires_coax():
    runCase(testdata_path, 'two_wires_coax')


def test_two_wires_open():
    runCase(testdata_path, 'two_wires_open')


def test_meshFromStep_with_two_wires_coax():
    gmsh.initialize()

    case_name = 'two_wires_coax'
    meshFromStep(inputFileFromCaseName(case_name), case_name)

    pGs = gmsh.model.getPhysicalGroups()
    assert (len(pGs) == 4)

    pGNames = [gmsh.model.getPhysicalName(*pG) for pG in pGs]
    assert ('Conductor_0' in pGNames)
    assert ('Conductor_1' in pGNames)
    assert ('Conductor_2' in pGNames)
    assert ('Vacuum' in pGNames)

    c0pG = getPhysicalGrupWithName('Conductor_0')
    c0ents = gmsh.model.getEntitiesForPhysicalGroup(*c0pG)
    assert (len(c0ents) == 1)

    # gmsh.fltk.run()  # for debugging only.
    gmsh.finalize()


def test_five_wires():
    runCase(testdata_path, 'five_wires')


def test_meshFromStep_with_five_wires():
    gmsh.initialize()

    case_name = 'five_wires'
    meshFromStep(inputFileFromCaseName(case_name), case_name)
    
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

    # gmsh.fltk.run()  # for debugging only.
    gmsh.finalize()


def test_three_wires_ribbon():
    runCase(testdata_path, 'three_wires_ribbon')


def test_nested_coax():
    runCase(testdata_path, 'nested_coax')


def test_agrawal1981():
    runCase(testdata_path, 'agrawal1981')


def test_stepShapes_for_partially_filled_coax():
    case_name = 'partially_filled_coax'

    gmsh.initialize()
    gmsh.model.add(case_name)
    stepShapes = ShapesClassification(
        gmsh.model.occ.importShapes(
            testdata_path + case_name + '/' + case_name + '.step'
        )
    )

    gmsh.finalize()

    assert (len(stepShapes.pecs) == 2)
    assert (len(stepShapes.dielectrics) == 1)


def test_stepShapes_for_five_wires():
    case_name = 'five_wires'

    gmsh.initialize()
    gmsh.model.add(case_name)
    stepShapes = ShapesClassification(
        gmsh.model.occ.importShapes(
            testdata_path + case_name + '/' + case_name + '.step'
        )
    )

    gmsh.finalize()

    assert (len(stepShapes.pecs) == 6)
    assert (len(stepShapes.dielectrics) == 5)


def test_stepShapes_for_three_wires_ribbon():
    case_name = 'three_wires_ribbon'

    gmsh.initialize()
    gmsh.model.add(case_name)
    stepShapes = ShapesClassification(
        gmsh.model.occ.importShapes(
            testdata_path + case_name + '/' + case_name + '.step'
        )
    )

    gmsh.finalize()

    assert (len(stepShapes.open) == 1)
    assert (len(stepShapes.pecs) == 3)
    assert (len(stepShapes.dielectrics) == 3)
