import sys
sys.path.append(".")

from qubit.data import atomnumber
from qubit.parsing.xyz import load_xyz_from_file
from qubit.preprocessing.descriptors import generate_coulomb_matrix


methane = r'C:\Users\Michiel Jacobs\Research\Master Thesis\Qubit\tests\test_data\butanol.xyz'

atoms, xyz = load_xyz_from_file(methane)
z = [atomnumber[atom] for atom in atoms]
m = generate_coulomb_matrix(z, xyz)
print(z)
print(m)
