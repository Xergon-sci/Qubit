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
            AttributeError: [description]
        """
        if self.negative_frequencies is None:
            raise AttributeError('This Gaussian file is not checked for negative (imaginary) frequencies, please check for this first by calling check_frequencies().')
    
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

    def extract_HOMO_energy(self):
        self._confirm_all()
        NotImplemented

    def extract_LUMO_energy(self):
        self._confirm_all()
        NotImplemented
