from qubit.parsing.xyz import XYZ
from qubit.data import atomnumber
import numpy as np

"""This module provides functionality to generate usefull molcular descriptors
that can be used in machine learning or deep learning.
"""


def generate_coulomb_matrix(file):
    """Generates the coulomb matrix from an XYZ file.

    Args:
        file (path): Path to the xyz file.

    Returns:
        (2darray): 2 dimensional array containing the coulomb matrix.
    """

    # parse the input z-matrix
    parser = XYZ()
    atoms, xyz = parser.load_xyz_from_file(file)

    # determine the lenght of the molecule and atomnumbers
    n = len(atoms)
    z = [atomnumber[atom] for atom in atoms]

    # create an empty matrix
    cm = np.zeros((n, n))

    # calculate the values, populate the array and return the coulomb matrix
    for i in range(n):
        for j in range(n):
            if i == j:
                cm[i][j] = 0.5 * z[i] ** 2.4
            elif i < j:
                cm[i][j] = (
                    z[i] * z[j] / (np.linalg.norm(np.array(xyz[i]) - np.array(xyz[j])))
                )
                cm[j][i] = cm[i][j]
    return cm


def randomize_coulomb_matrix(coulomb_matrix):
    """Randomizes the coulomb matrix.

    Args:
        coulomb_matrix (2darray): The coulomb matrix to randomize.

    Returns:
        (2darray): The randomized coulomb matrix.
    """
    # calculate the row normals of a coulomb matrix
    row_norms = np.array([np.linalg.norm(row) for row in coulomb_matrix], dtype=float)

    # draw random numbers from a normal distribution
    rand = np.random.RandomState()
    n = rand.normal(size=row_norms.size)

    # calcualte the permutation
    p = np.argsort(row_norms + n)

    # Permute row wise then coulomn wise
    return coulomb_matrix[p][:, p]
