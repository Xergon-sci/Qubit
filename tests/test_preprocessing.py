from qubit.preprocessing.matrix_operations import pad_matrix
import numpy as np

def test_matrix_padding():
    m = pad_matrix(np.zeros((5,5)), 10)
    assert m.shape == np.zeros((10,10)).shape