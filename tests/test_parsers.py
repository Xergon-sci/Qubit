import unittest
import os
from qubit.parsers.zmatrix import ZMatrix

CUR_DIR = os.path.dirname(os.path.abspath(__file__))

class TestZMatrixOperations(unittest.TestCase):

    def setUp(self):
        self.parser = ZMatrix()
        self.methane = os.path.join(CUR_DIR, 'test_data/methane.xyz')

    def test_load_zmatrix_from_file(self):
        atomsCheck = ['C', 'H', 'H', 'H', 'H']
        xyzCheck = [['0.000000', '0.000000', '0.000000'],
        ['0.000000', '0.000000', '1.089000'],
        ['1.026719', '0.000000', '-0.363000'],
        ['-0.513360', '-0.889165', '-0.363000'],
        ['-0.513360', '0.889165', '-0.363000']]
        
        atoms, xyz = self.parser.load_zmatrix_from_file(self.methane)
        self.assertEqual(atomsCheck, atoms)
        self.assertEqual(xyzCheck, xyz)

if __name__ == '__main__':
    unittest.main()