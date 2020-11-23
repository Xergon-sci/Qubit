import os
import mmap

"""This submodule aims to provide utilities for the gaussian software package.
It will allow the user to quickly write custom interfaces to analyse the output files.
"""

class Extractor:
    """This class supports data extraction from gaussian output files.
    It provides functionality to extract all the implemented data at once or custom extraction
    can be set up by using its public methods.
    """

    def __init__(self, filepath):
        self.filepath = filepath
        self.normal_execution = None
        self.negative_frequencies = None
        self.convergence = None

    def _find_last_occurance(self, word):
        """Support function that finds the last occurance of a word in a file.

        Args:
            word (str): Word to search for in the file.

        Returns:
            mmap: Returns mmap located at the line the last occurance of {word} is at.
        """
        with open(self.filepath, "r") as f:
            m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        i = m.rfind(str.encode(word))
        m.seek(i)
        return m

    def _confirm_normal_execution(self):
        """Confirms the normal execution of the current Gaussian file.

        Raises:
            AttributeError: Raises when no check for normal execution has occured.
        """
        if self.normal_execution is None:
            raise AttributeError('This Gaussian file is not checked for normal execution, please check for this first by calling check_normal_execution().')

    def _confirm_negative_frequencies(self):
        """Cofirms there are no imaginary frequencies found on the current Gaussian file.

        Raises:
            AttributeError: Raises when no check for negative (imaginary) frequencies has occured.
        """
        if self.negative_frequencies is None:
            raise AttributeError('This Gaussian file is not checked for negative (imaginary) frequencies, please check for this first by calling check_frequencies().')
    
    def _confirm_convergence(self):
        """Cofirms there is convergence in the current Gaussian file.

        Raises:
            AttributeError: Raises when no check for convergence has occured.
        """
        if self.convergence is None:
            raise AttributeError('This Gaussian file is not checked for convergence, please check for this first by calling check_convergence().')

    def _confirm_all(self):
        """Bundlefunction that confirms all requirements.
        """
        self._confirm_normal_execution()
        self._confirm_negative_frequencies()

    def check_normal_execution(self):
        """Checks for normal execution

        Checks for normal execution of the gaussian output file.
        Use this first when writing custom extraction methods to check the validity of the calculations.

        Returns:
            (bool): Returns True when a calculation has normal execution.
        """
        with open(self.filepath, "rb") as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
            line = f.readline().decode()
            if "Normal termination of Gaussian" in line:
                self.normal_execution = True
                return True
            else:
                self.normal_execution = False
                raise Exception('This Gaussian file has no normal execution. Fix these errors first in Gaussian.')
    
    def check_frequencies(self):
        """Check for negative (imaginary) frequencies.
        
        Returns:
            (bool): Returns False if no negative frequencies are found.

        Raises:
            Exception: Raises when negative frequencies are found.
        """
        self._confirm_normal_execution()
        m = self._find_last_occurance('Frequencies --')
        split = m.readline().split()
        
        for i in range(2,5):
            x = float(bytes.decode(split[i]))
            if x < 0:
                raise Exception('Negative frequency found. Manual revision is advised.')
        self.negative_frequencies = False
        return False

    def check_convergence(self):
        """Check for convergence errors.

        Returns:
            (bool): Returns True if convergence is reached.
        """
        self._confirm_normal_execution()
        self._confirm_negative_frequencies()
        try:
            self._find_last_occurance('Convergence criterion not met.')
        except ValueError:
            self.convergence = True
        else:
            self.convergence = False
            raise Exception('The convergence criterion of this Gaussian file are not met.')
        return self.convergence

    def extract_optimized_geometry(self):
        """Extracts the optimized geometry

        Extracts the optimized geometry from the gaussian output file.

        Returns:
            (tuple): tuple containing:

                atoms (list) : Atom numbers
                coördinates (list): Cartesian coordinates in a 2D list
        """
        self._confirm_all()
        m = self._find_last_occurance('Standard orientation')
        m.readline()
        m.readline()
        m.readline()
        m.readline()
        m.readline()

        atoms = []
        xyz = []
        is_molecule = True
        while is_molecule:
            # read and process the line
            line = bytes.decode(m.readline())
            split = line.split()

            # check if is still the molecule
            if len(split) == 1:
                is_molecule = False
            else:
                # process the line
                atoms.append(split[1])
                coords = []
                coords.append(split[3])
                coords.append(split[4])
                coords.append(split[5])
                xyz.append(coords)
        return atoms, xyz

    def extract_SCF(self):
        import re
        self._confirm_all()
        with open(self.filepath, "r") as f:
            m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

        [print(s) for s in re.finditer(b'Proceeding to internal job step number', m)]

        # Determine all links and find line numbers
        # Find all SCF Done's, above each link statement


    def extract_HOMO_energy(self):
        self._confirm_all()
        NotImplemented

    def extract_LUMO_energy(self):
        self._confirm_all()
        NotImplemented
