import gmsh
import os

from src.step2gmsh import *

import sys

sys.path.insert(0, '.')


dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'
testdata_path = dir_path + '/../testData/'

def test_launcher():
    case_name = 'partially_filled_coax'
    input = testdata_path + case_name + '/' + case_name + '.step'
    launcher(input)
