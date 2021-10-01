class Parser:
    """Parent class for all parsers.
    """

    def load(self):
        """Placeholder

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def write(self):
        """Placeholder

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

class XYZ(Parser):
    """Parser for parsing XYZ files.
    """
    
    def load(self, file):
        """Load the molecule from an XYZ file.

        Args:
            file (string): Name of the file or path to were it is located.

        Returns:
            (list, list): Returns a list of atoms and a 2D list of coordinates.
        """
        atoms = []
        coordinates = []
        with open(file, "r") as matrix:
            for line, content in enumerate(matrix):
                n = 0
                xyz = []

                # the first line contains typically the atom count
                if line == 0:
                    continue
                # the second line is empty or contains a title
                elif line == 1:
                    continue
                else:
                    for word in content.split():
                        # the other lines contain the molecular data
                        if n == 0:
                            atoms.append(word)
                        elif n > 0:
                            xyz.append(float(word))
                        n = n + 1
                coordinates.append(xyz)
        return atoms, coordinates