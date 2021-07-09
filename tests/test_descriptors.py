import os
import pytest
import numpy as np
from qubit.descriptors import Descriptor
from qubit.descriptors import CoulombMatrix

@pytest.fixture
def descriptor():
    return Descriptor()

def test_generate(descriptor):
    with pytest.raises(Exception) as e:
        descriptor.generate()

def test_normalize(descriptor):
    with pytest.raises(Exception) as e:
        descriptor.normalize()

atoms = ['C', 'H', 'H', 'H', 'H']
xyz = [
    [0.000000, 0.000000, 0.000000],
    [0.000000, 0.000000, 1.089000],
    [1.026719, 0.000000, -0.363000],
    [-0.513360, -0.889165, -0.363000],
    [-0.513360, 0.889165, -0.363000]]
 
@pytest.fixture
def coulombMatrix():
    return CoulombMatrix()

def test_coulomb_matrix(coulombMatrix):
    cm = coulombMatrix.generate(atoms, xyz)
    assert cm.size != 0

def test_coulomb_matrix_randomize(coulombMatrix):
    cm = coulombMatrix.generate(atoms, xyz, randomize=True)
    assert cm.size != 0

def test_randomize_coulomb_matrix(coulombMatrix):
    cm = coulombMatrix.normalize(np.random.rand(5,5))
    assert cm.size != 0

def test_pad_matrix(coulombMatrix):
    pass

def test_normalize(coulombMatrix):
    pass