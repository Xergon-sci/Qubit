import os
import mmap

class Extractor:
    """This class supports the extraction of data from gaussian output files.
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def _find_last_occurance(self, word):
        with open(self.filepath, "r") as f:
            m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        i = m.rfind(str.encode(word))
        m.seek(i)
        return m

    def check_normal_execution(self):
        """Checks for normal execution of the gaussian output file.
        Use this first when writing custom extraction methods to validate the file.

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

    def extract_cartesian_coordinates(self):
        """Extracts the optimized geometry from a gaussian output file.

        Returns:
            Array: Returns 2 arrays, one containng the atom numbers and onother containing the XYZ coordinates.
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
