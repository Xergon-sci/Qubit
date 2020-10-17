from qubit.descriptors import CoulombMatrix
import numpy as np
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
methane = os.path.join(CUR_DIR, 'test_data/methane.xyz')

def test_coulomb_matrix():
    cm = CoulombMatrix()
    m = cm.generate_coulomb_matrix(methane)
    assert np.any(m != None)