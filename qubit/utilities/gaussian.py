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

    def _find_last_occurance(self, word):
        """Support function that find the last occurance of a word in a file.

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

    def check_normal_execution(self):
        """Checks for normal execution of the gaussian output file.
        Use this first when writing custom extraction methods to check the validity of the calculations.

        Returns:
            Boolean: Returns True when a calculation has normal execution.
        """
        with open(self.filepath, "rb") as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
            line = f.readline().decode()
            if "Normal termination of Gaussian" in line:
                return True
            else:
                return False

    def extract_optimized_geometry(self):
        """Extracts the optimized geometry from the gaussian output file.

        Returns:
            List: List with the atom numbers of the atoms.
            List: List with the cartesian coordinates of the atoms.
        """
        m = self._find_last_occurance("Standard orientation")
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

    def extract_HOMO_energy():
        NotImplemented

    def extract_LUMO_energy():
        NotImplemented

    def extract(self):
        # check normal termination
        if not self.check_normal_execution():
            raise ValueError(
                "Gaussian did not terminate normal. In: {}".format(self.filepath)
            )

        # extract gaussian data
