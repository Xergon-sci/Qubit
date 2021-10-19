import os
import pytest
import numpy as np
from qubit.descriptors import Descriptor
from qubit.descriptors import CoulombMatrix
from qubit.descriptors import CoulombVector

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

def test_coulomb_matrix():
    cm = CoulombMatrix.generate(atoms, xyz)
    assert cm.size != 0

def test_coulomb_matrix_randomize():
    cm = CoulombMatrix.generate(atoms, xyz, randomize=True)
    assert cm.size != 0

def test_randomize_coulomb_matrix():
    cm = CoulombMatrix.generate(atoms, xyz)
    rcm = CoulombMatrix.randomize(cm)
    assert rcm.size == cm.size

def test_pad_matrix():
    cm = CoulombMatrix.generate(atoms, xyz)
    pcm = CoulombMatrix.pad_matrix(cm, 10)
    assert pcm.shape[0] == 10

def test_normalize():
    cm = CoulombMatrix.generate(atoms, xyz)
    tensor = CoulombMatrix.normalize(cm, negative_dimensions=1, positive_dimensions=1)
    assert tensor.shape == (3,5,5)

def test_coulomb_vector():
    cv = CoulombVector.generate(atoms, xyz)
    assert cv.shape[1] == len(atoms)+1


def test_coulomb_vector_randomize():
    cv = CoulombVector.generate(atoms, xyz)
    rcv = CoulombVector.randomize(cv)
    assert rcv.shape == cv.shape

def test_pad_matrix():
    cvs = CoulombVector.generate(atoms, xyz)
    pcv = CoulombVector.pad_vector(cvs[0], 10)
    assert pcv.shape[0] == 10

def test_vector_normalize():
    cvs = CoulombVector.generate(atoms, xyz)
    tensor = CoulombVector.normalize(cvs[0], positive_dimensions=1, negative_dimensions=1)
    assert tensor.shape == (3, cvs[0].shape[0])