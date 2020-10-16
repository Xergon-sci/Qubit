import numpy as np

class ZMatrix:

    def __init__(self):
        pass

    def load_zmatrix_from_file(self, file):
        atoms = []
        coordinates = []
        with open(file, 'r') as matrix:
            for line in matrix:
                n = 0
                xyz = []
                for word in line.split():
                    if n == 0:
                        atoms.append(word)
                    elif n > 0:
                        xyz.append(float(word))
                    n = n + 1
                coordinates.append(xyz)
        return atoms, coordinates
