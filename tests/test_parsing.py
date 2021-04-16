import os
from qubit.parsing import XYZ

methane = os.path.join(os.path.dirname(__file__), 'test_data/methane.xyz')

def test_XYZ_load():
    atoms = ['C', 'H', 'H', 'H', 'H']
    xyz = [
        [0.000000, 0.000000, 0.000000],
        [0.000000, 0.000000, 1.089000],
        [1.026719, 0.000000, -0.363000],
        [-0.513360, -0.889165, -0.363000],
        [-0.513360, 0.889165, -0.363000]]
    
    parser = XYZ()
    p_atoms, p_xyz = parser.load(methane)

    assert p_atoms == atoms
    assert p_xyz == xyz