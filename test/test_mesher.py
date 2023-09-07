import gmsh
import os
from src.mesher import *
import sys

sys.path.insert(0, '.')


dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
testdata_path = dir_path + '/../testData/'


def test_getNumberFromEntityName():
    assert (ShapesClassification.getNumberFromEntityName(
        'Shapes/Conductor_1',
        'Conductor_') == 1
    )

    assert (ShapesClassification.getNumberFromEntityName(
        'Shapes/solid_wire_002/Conductor_002/Conductor_002',
        'Conductor_') == 2
    )


def test_partially_filled_coax():
    meshFromStep(testdata_path, 'partially_filled_coax')


def test_empty_coax():
    meshFromStep(testdata_path, 'empty_coax')


def test_two_wires_coax():
    meshFromStep(testdata_path, 'two_wires_coax')


def test_five_wires():
    meshFromStep(testdata_path, 'five_wires')


def test_three_wires_ribbon():
    meshFromStep(testdata_path, 'three_wires_ribbon')


def test_nested_coax():
    meshFromStep(testdata_path, 'nested_coax')


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
