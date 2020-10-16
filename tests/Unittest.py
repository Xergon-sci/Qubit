import unittest
from qubit.parsers.zmatrix import zmatrix

class TestParsers(unittest.TestCase):

    def test_matrix(self):
        parser = zmatrix()
        atomsCheck = ['C', 'H', 'H', 'H', 'H']
        xyzCheck = [['0.000000', '0.000000', '0.000000'],
        ['0.000000', '0.000000', '1.089000'],
        ['1.026719', '0.000000', '-0.363000'],
        ['-0.513360', '-0.889165', '-0.363000'],
        ['-0.513360', '0.889165', '-0.363000']]
        
        atoms, xyz = parser.load_zmatrix_from_file('/data/brussel/102/vsc10255/qubit/tests/test.xyz')
        self.assertEqual(atomsCheck, atoms)
        self.assertEqual(xyzCheck, xyz)

if __name__ == '__main__':
    unittest.main()