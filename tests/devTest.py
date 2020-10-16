from qubit.parsers.xyz import XYZ
from qubit.descriptors import CoulombMatrix

cm = CoulombMatrix()

print(cm.generate_coulomb_matrix('/data/brussel/102/vsc10255/qubit/tests/test_data/methane.xyz'))