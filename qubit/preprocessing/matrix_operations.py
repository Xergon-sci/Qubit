import numpy as np
import warnings

"""This module is a support module for matrix operations.
"""


def pad_matrix(matrix, size):
    """Applies padding to a matrix.

    You can use this function to scale a matrix to a given size.
    The empty space is filled with zeros.

    Example: Can be used to pad the Coulomb Matrix.

    Args:
        matrix (2D np.array): Matrix to pad in a nested list format.
        size (int): The size to scale the matrix to.

    Returns:
        ndarray: The padded matrix.
    """
    if isinstance(matrix, list):
        matrix = np.array(list)

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
