import numpy as np

def matrix_padding(matrix, size):
    m = np.pad(matrix, (0, size))
    return m