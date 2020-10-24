from qubit.descriptors import CoulombMatrix
from qubit.preprocessing.matrix_operations import matrix_padding
import numpy as np

cm = CoulombMatrix()
coulombMatrix = cm.generate_coulomb_matrix('/data/brussel/102/vsc10255/qubit/tests/test_data/methane.xyz')
print("Randomized:")
print(cm.randomize_coulomb_matrix(coulombMatrix))