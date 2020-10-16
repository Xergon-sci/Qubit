import os
from qubit.parsers.zmatrix import ZMatrix

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
methane = os.path.join(CUR_DIR, 'test_data/methane.xyz')

def test_load_zmatrix_from_file():
    parser = ZMatrix()
    atomsCheck = ['C', 'H', 'H', 'H', 'H']
    xyzCheck = [[0.0, 0.0, 0.0],
    [0.0, 0.0, 1.089],
    [1.026719, 0.0, -0.363],
    [-0.51336, -0.889165, -0.363],
    [-0.51336, 0.889165, -0.363]]
    
    atoms, xyz = parser.load_zmatrix_from_file(methane)
    assert atoms == atomsCheck
    assert xyz == xyzCheck