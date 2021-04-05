from qubit.data import atomnumber
import numpy as np
import math

"""This module provides functionality to generate usefull molcular descriptors
that can be used in machine learning or deep learning.
"""


def generate_coulomb_matrix(atoms, xyz):
    """Generates the coulomb matrix from an atoms and xyz matrix.

    Generates the coulomb matrix from an atoms and xyz matrix. Can be loaded in by using load_xyz_from_file().
    convert atoms symbols to numbers with z = [atomnumber[atom] for atom in atoms]

    Args:
        file (path): Path to the xyz file.

    Returns:
        (2darray): 2 dimensional array containing the coulomb matrix.
    """
    # determine the lenght of the molecule and atomnumbers
    n = len(atoms)
    z = atoms
    print(z[0])

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

def tensorise_coulomb_matrix(coulomb_matrix, phi=1, slope=0.7, negative_dimensions=0, positive_dimension=0):
    tensors = []
    cm = np.array(coulomb_matrix)

    # generate negative layers
    for i in range(negative_dimensions):
        tensor = np.empty([cm.shape[0],cm.shape[1]])
        for iy,y in enumerate(coulomb_matrix):
            for ix,x in enumerate(y):
                tensor[ix,iy] = (1/2)+((1/2)*math.tanh(((x-(i*phi))/phi)*slope))
        tensors.append(tensor)
    
    # generate base layer
    tensor = np.empty([cm.shape[0],cm.shape[1]])
    for iy,y in enumerate(coulomb_matrix):
        for ix,x in enumerate(y):
            tensor[ix,iy] = (1/2)+((1/2)*math.tanh((x/phi)*slope))
    tensors.append(tensor)

    # generate negapositive layers
    for i in range(positive_dimension):
        tensor = np.empty([cm.shape[0],cm.shape[1]])
        for iy,y in enumerate(coulomb_matrix):
            for ix,x in enumerate(y):
                tensor[ix,iy] = (1/2)+((1/2)*math.tanh(((x+(i*phi))/phi)*slope))
        tensors.append(tensor)
    return np.array(tensors)

def generate_coulomb_vectors(atoms, xyz):

    # determine the lenght of the molecule and atomnumbers
    n = len(atoms)

    if type(atoms[0]) == str:
    z = [atomnumber[atom] for atom in atoms]
    else:
        z = atoms

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