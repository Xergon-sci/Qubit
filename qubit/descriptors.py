from parsers.zmatrix import ZMatrix
from qubit.data import atomnumber


class CoulombMatrix:

    def generate_coulomb_matrix(self, file):
        parser = ZMatrix()
        atoms, xyz = parser.load_zmatrix_from_file(file)

    def get_atom_count(self, atoms):
        return len(atoms)

    def get_atom_number(self, atom):
        return atomnumber[atom]
