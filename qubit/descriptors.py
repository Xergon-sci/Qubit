import warnings
import math
import numpy as np
from qubit.data import atomnumber
from qubit.data import atomsymbol
import random

class Descriptor:
    """Parent class for all descriptors
    """
    
    def generate(self):
        """Placeholder

        Raises:
            NotImplementedError
        """
        raise NotImplementedError
    
    def normalize(self):
        """Placeholder

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

class CoulombMatrix(Descriptor):
    """Provides functionality to generate the Coulomb Matrix (1).

    (1) Montavon, G.; Hansen, K.; Fazli, S.; Rupp, M.; Biegler, F.; Ziehe, A.;
    Tkatchenko, A.; Lilienfeld, A.; Müller, K.-R.
    Learning Invariant Representations of Molecules for Atomization Energy Prediction.
    In Advances in Neural Information Processing Systems;
    Pereira, F., Burges, C. J. C., Bottou, L., Weinberger, K. Q., Eds.;
    Curran Associates, Inc., 2012; Vol. 25.
    """

    def generate(atoms, xyz, randomize=False):
        """Generates the Coulomb Matrix (1).

        (1) Montavon, G.; Hansen, K.; Fazli, S.; Rupp, M.; Biegler, F.; Ziehe, A.;
        Tkatchenko, A.; Lilienfeld, A.; Müller, K.-R.
        Learning Invariant Representations of Molecules for Atomization Energy Prediction.
        In Advances in Neural Information Processing Systems;
        Pereira, F., Burges, C. J. C., Bottou, L., Weinberger, K. Q., Eds.;
        Curran Associates, Inc., 2012; Vol. 25.

        Args:
            atoms (list): A list of atoms.
            xyz (2D list): A list of 3D coordinates.

        Returns:
            2D list: The Coulomb Matrix.
        """
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
                        z[i] * z[j] /
                        (np.linalg.norm(np.array(xyz[i]) - np.array(xyz[j])))
                    )
                    cm[j][i] = cm[i][j]

        if randomize:
            return CoulombMatrix.randomize(cm)
        else:
            return cm

    def randomize(coulomb_matrix):
        """Randomizes the Coulomb Matrix as described in (1).

        (1) Montavon, G.; Hansen, K.; Fazli, S.; Rupp, M.; Biegler, F.; Ziehe, A.;
        Tkatchenko, A.; Lilienfeld, A.; Müller, K.-R.
        Learning Invariant Representations of Molecules for Atomization Energy Prediction.
        In Advances in Neural Information Processing Systems;
        Pereira, F., Burges, C. J. C., Bottou, L., Weinberger, K. Q., Eds.;
        Curran Associates, Inc., 2012; Vol. 25.

        Args:
            coulomb_matrix (2D list): The Coulomb Matrix as generated in :func:`~Qubit.descriptors.CoulombMatrix.generate`

        Returns:
            2D list: The randomized Coulomb Matrix.
        """
        # calculate the row normals of a coulomb matrix
        row_norms = np.array([np.linalg.norm(row)
                              for row in coulomb_matrix], dtype=float)

        # draw random numbers from a normal distribution
        rand = np.random.RandomState()
        n = rand.normal(size=row_norms.size)

        # calcualte the permutation
        p = np.argsort(row_norms + n)

        # Permute row wise then coulomn wise
        return coulomb_matrix[p][:, p]

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

    def normalize(coulomb_matrix, phi=1, negative_dimensions=0, positive_dimensions=0):
        """Normalizes the Coulomb Matrix by tensorizing it. May require padding.
        This method is an adaption from (1).

        (1) Montavon, G.; Hansen, K.; Fazli, S.; Rupp, M.; Biegler, F.; Ziehe, A.;
        Tkatchenko, A.; Lilienfeld, A.; Müller, K.-R.
        Learning Invariant Representations of Molecules for Atomization Energy Prediction.
        In Advances in Neural Information Processing Systems;
        Pereira, F., Burges, C. J. C., Bottou, L., Weinberger, K. Q., Eds.;
        Curran Associates, Inc., 2012; Vol. 25.


        Args:
            coulomb_matrix (2D list): The Coulomb Matrix.
            phi (int, optional): Equivalent to an offset. Defaults to 1.
            negative_dimensions (int, optional): The amount of negative dimensions describing the tensor. Defaults to 0.
            positive_dimension (int, optional): The amount of positive dimensions describing the tensor. Defaults to 0.

        Returns:
            2D list: Tensorized Coulomb Matrix.
        """
        tensors = []
        cm = np.array(coulomb_matrix)

        def sigmoid(x):
            return np.exp(x) / (1 + np.exp(x))

        # generate negative layers
        for i in range(-negative_dimensions, 0):
            tensor = sigmoid((cm + (i * phi)) / phi) # i = negative here
            tensors.append(tensor)

        # generate base layer
        tensor = sigmoid(cm / phi)
        tensors.append(tensor)

        # generate negapositive layers
        for i in range(positive_dimensions):
            tensor = sigmoid((cm + (i * phi)) / phi)
            tensors.append(tensor)
        return np.array(tensors)

class CoulombVector(Descriptor):
    """Provides functionality to generate the Coulomb Vector.
    """

    def generate(atoms, xyz):
        # determine the lenght of the molecule and atomnumbers
        n = len(atoms)

        if type(atoms[0]) == str:
            z = [atomnumber[atom] for atom in atoms]
        else:
            z = atoms

        # create an empty matrix
        cm = np.zeros((n, n+1))

        # calculate the values, populate the array and return the coulomb matrix
        for i in range(n):
            for j in range(n+1):
                if i == j:
                    cm[i][j] = 0.5 * z[i] ** 2.4
                elif j == n:
                    cm[i][j] = z[i]
                elif i < j:
                    cm[i][j] = (
                        z[i] * z[j] /
                        (np.linalg.norm(np.array(xyz[i]) - np.array(xyz[j])))
                    )
                    cm[j][i] = cm[i][j]
        return cm

    def randomize(coulomb_vector):
        """Randomizes the Coulomb Vector.
        """
        random.shuffle(coulomb_vector)
        return coulomb_vector

    def pad_vector(vector, size):
        """Applies padding to a vector.

        You can use this function to scale a vector to a given size.
        The empty space is filled with zeros.

        Example: Can be used to pad the Coulomb Vector.

        Args:
            matrix (2D np.array): Matrix to pad in a nested list format.
            size (int): The size to scale the matrix to.

        Returns:
            ndarray: The padded vector.
        """
        if isinstance(vector, list):
            vector = np.asarray(vector)

        # calculate the wished size
        size = size - vector.size
        print(size)

        # confirm the size isn't less than the default matrix size
        if size <= 0:
            m = vector
            warnings.warn(
                "Trying to reduce the matrix size, default matrix size has been returned!",
                Warning,
            )
        else:
            # pad the matrix
            m = np.pad(vector, (0, size))
        return m

    def normalize(coulomb_vector, phi=1, negative_dimensions=0, positive_dimensions=0):
        return CoulombMatrix.normalize(
            coulomb_vector,
            phi=phi,
            negative_dimensions=negative_dimensions,
            positive_dimensions=positive_dimensions)