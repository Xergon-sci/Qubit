class zmatrix:

    def __init__(self):
        pass

    def loadzmatrixfromFile(self, file):
        with open(file, 'r') as matrix:
            for line in matrix:
                print(line)