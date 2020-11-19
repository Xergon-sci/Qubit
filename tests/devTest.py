from qubit.utilities.gaussian import Extractor

extractor = Extractor('/data/brussel/102/vsc10255/data/datasets/CNOS_sub1_10to20_10k/calculations/gaussian_output/JID_0.log')
print(extractor.check_normal_execution())