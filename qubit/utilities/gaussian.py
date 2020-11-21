import os
import mmap

"""
.. module:: useful_1
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Andrew Carter <andrew@invalid.com>


"""

def testdoc():
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
    NotImplemented

class Extractor:
    def __init__(self, filepath):
        self.filepath = filepath

    def find_last_occurance(self, word):
        with open(self.filepath, "r") as f:
            m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        i = m.rfind(str.encode(word))
        m.seek(i)
        return m

    def check_normal_execution(self):
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
        m = self.find_last_occurance("Standard orientation")
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
