import numpy as np
import warnings


def matrix_padding(matrix, size):
    # calculate the wished size
    size = size - matrix.shape[0]

    # confirm the size isn't less than the default matrix size
    if size <= 0:
        m = matrix
        warnings.warn(
            "Trying to reduce the matrix size, default matrix size has been returned!",
            Warning,
        )
    else:
        # pad the matrix
        m = np.pad(matrix, (0, size))
    return m
