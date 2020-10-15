class zmatrix:

    def __init__(self):
        pass

    def loadzmatrixfromFile(self, file):
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
                        print(word)
                        # Continue here
                    coordinates.append(xyz)
                    n = n + 1

        return atoms, coordinates
