from qubit.utilities.gaussian import Extractor

ex = Extractor('/data/brussel/102/vsc10255/qubit/tests/test_data/JID_0.log')

ex.check_normal_execution()
print(ex.check_frequencies())