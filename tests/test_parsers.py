import os
from qubit.parsers.zmatrix import ZMatrix

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
methane = os.path.join(CUR_DIR, 'test_data/methane.xyz')

def test_load_zmatrix_from_file():
    parser = ZMatrix()
    atomsCheck = ['C', 'H', 'H', 'H', 'H']
    xyzCheck = [['0.000000', '0.000000', '0.000000'],
    ['0.000000', '0.000000', '1.089000'],
    ['1.026719', '0.000000', '-0.363000'],
    ['-0.513360', '-0.889165', '-0.363000'],
    ['-0.513360', '0.889165', '-0.363000']]
    
    atoms, xyz = parser.load_zmatrix_from_file(methane)
    assert atoms == atomsCheck
    assert xyz == xyzCheck