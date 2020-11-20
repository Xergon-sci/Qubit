import numpy as np


class XYZ:
    def __init__(self):
        pass

    def load_xyz_from_file(self, file):
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
