from qubit.preprocessing.matrix_operations import matrix_padding
import numpy as np

def test_matrix_padding():
    m = matrix_padding(np.zeros((5,5)), 10)
    assert m.shape == np.zeros((10,10)).shape