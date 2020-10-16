from qubit.parsers.zmatrix import ZMatrix
from qubit.descriptors import CoulombMatrix

cm = CoulombMatrix()

print(cm.generate_coulomb_matrix('/data/brussel/102/vsc10255/qubit/tests/test_data/methane.xyz'))

import os
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
methane = os.path.join(CUR_DIR, 'test_data/methane.xyz')

parser = ZMatrix()

atoms, xyz = parser.load_zmatrix_from_file(methane)

print(xyz)