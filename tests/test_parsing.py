import os
import pytest
from qubit.parsing import Parser
from qubit.parsing import XYZ

methane = os.path.join(os.path.dirname(__file__), 'test_data/methane.xyz')

@pytest.fixture
def parser():
    return Parser()

def test_default_load(parser):
    with pytest.raises(Exception) as e:
        parser.load()

def test_default_write(parser):
    with pytest.raises(Exception) as e:
        parser.write()

@pytest.fixture
def xyz_parser():
    return XYZ()

def test_XYZ_load(xyz_parser):
    atoms = ['C', 'H', 'H', 'H', 'H']
    xyz = [
        [0.000000, 0.000000, 0.000000],
        [0.000000, 0.000000, 1.089000],
        [1.026719, 0.000000, -0.363000],
        [-0.513360, -0.889165, -0.363000],
        [-0.513360, 0.889165, -0.363000]]

    p_atoms, p_xyz = xyz_parser.load(methane)

    assert (p_atoms, p_xyz) == (atoms, xyz)