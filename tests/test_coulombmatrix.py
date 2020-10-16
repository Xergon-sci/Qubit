from qubit.descriptors import CoulombMatrix

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
methane = os.path.join(CUR_DIR, 'test_data/methane.xyz')

def test_coulomb_matrix():
    cmCheck = [[36.8581052, 5.50964187, 5.50964209, 5.50963981, 5.50963981],
    [5.50964187, 0.5, 0.56232548, 0.56232539, 0.56232539],
    [5.50964209, 0.56232548, 0.5, 0.56232532, 0.56232532],
    [5.50963981, 0.56232539, 0.56232532, 0.5, 0.56232533],
    [5.50963981, 0.56232539, 0.56232532, 0.56232533, 0.5]]
    cm = CoulombMatrix()
    assert cm.generate_coulomb_matrix(methane) == cmCheck