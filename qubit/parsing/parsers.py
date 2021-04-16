class XYZ():
    '''
    test docstring
    '''

    def load(self, file):
        """Loads XYZ data from file.

        Args:
            file (filepath): Path to the file to load.

        Returns:
            (tuple): tuple containing:

                    atoms (list) : Atom numbers
                    coördinates (list): Cartesian coordinates in a 2D list
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
                # the second line is empty
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