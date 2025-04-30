import numpy as np
def assertListOfFloatsAlmostEqual(realValues, expectedValues, tolerance = 0.0000001):
    if len(realValues) != len(expectedValues):
        raise AssertionError("List have diferent lengths: {} != {}".format(len(realValues), len(expectedValues)))
    
    if not np.allclose(realValues, expectedValues, atol=tolerance):
        raise AssertionError("List are not the same: {} != {}".format(realValues, expectedValues))