from qubit.preprocessing.descriptors import generate_coulomb_matrix
from qubit.preprocessing.descriptors import randomize_coulomb_matrix
import numpy as np
import os

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
methane = os.path.join(CUR_DIR, 'test_data/methane.xyz')

def test_coulomb_matrix():
    m = generate_coulomb_matrix(methane)
    rm = randomize_coulomb_matrix(m)
    assert np.any(m != None)
    assert np.any(rm != None)