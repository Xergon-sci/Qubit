from parsers.zmatrix import zmatrix

mat = zmatrix()
atoms, xyz = mat.loadzmatrixfromFile('/data/brussel/102/vsc10255/qubit/tests/test.xyz')

print(atoms)
print(xyz)