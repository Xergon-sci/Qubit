import os
from qubit.utilities.gaussian import Extractor

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
gaussian_output = os.path.join(CUR_DIR, 'test_data/JID_0.log')

def test_extractor():
    ext = Extractor(gaussian_output)
    assert ext.check_normal_execution() == True