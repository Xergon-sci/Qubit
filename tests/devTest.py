from qubit.utilities.gaussian import Extractor

labels = ['neutraal', 'Energie_neutraal', 'Energie_kation', 'Energie_anion']
ex = Extractor('/data/brussel/102/vsc10255/qubit/tests/test_data/JID_0.log', labels=labels)
print(ex.extract_SCF())