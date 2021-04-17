import warnings
import math
import numpy as np
from qubit.data import atomnumber


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

    def generate(self, atoms, xyz, randomize=False):
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
        z = atoms

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
            return self.randomize(cm)
        else:
            return cm

    def randomize(self, coulomb_matrix):
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

    def normalize(coulomb_matrix, phi=1, slope=0.7, negative_dimensions=0, positive_dimension=0):
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
            slope (float, optional): The slope of the binarization function. Defaults to 0.7.
            negative_dimensions (int, optional): The amount of negative dimensions describing the tensor. Defaults to 0.
            positive_dimension (int, optional): The amount of positive dimensions describing the tensor. Defaults to 0.

        Returns:
            2D list: Tensorized Coulomb Matrix.
        """
        tensors = []
        cm = np.array(coulomb_matrix)

        # generate negative layers
        for i in range(negative_dimensions):
            tensor = np.empty([cm.shape[0], cm.shape[1]])
            for iy, y in enumerate(coulomb_matrix):
                for ix, x in enumerate(y):
                    tensor[ix, iy] = (
                        1/2)+((1/2)*math.tanh(((x-(i*phi))/phi)*slope))
            tensors.append(tensor)

        # generate base layer
        tensor = np.empty([cm.shape[0], cm.shape[1]])
        for iy, y in enumerate(coulomb_matrix):
            for ix, x in enumerate(y):
                tensor[ix, iy] = (1/2)+((1/2)*math.tanh((x/phi)*slope))
        tensors.append(tensor)

        # generate negapositive layers
        for i in range(positive_dimension):
            tensor = np.empty([cm.shape[0], cm.shape[1]])
            for iy, y in enumerate(coulomb_matrix):
                for ix, x in enumerate(y):
                    tensor[ix, iy] = (
                        1/2)+((1/2)*math.tanh(((x+(i*phi))/phi)*slope))
            tensors.append(tensor)
        return np.array(tensors)