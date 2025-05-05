import os
import step2gmsh

import sys

sys.path.insert(0, '.')


dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
testdata_path = dir_path + '/../testData/'

def test_launcher():
    case_name = 'partially_filled_coax'
    input = testdata_path + case_name + '/' + case_name + '.step'
    step2gmsh.launcher(input)
