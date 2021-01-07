from qubit.utilities.gaussian import Extractor

labels = ['neutraal', 'Energie_neutraal', 'Energie_kation', 'Energie_anion']
ex = Extractor('/data/brussel/102/vsc10255/data/CNOS_sub1_10to20_10k/calculations/gaussian_output/JID_1.log', labels=labels)

print('Optimized geometry:', ex.extract_optimized_geometry())
print('HOMO:', ex.extract_HOMO_energy())
print('LUMO:', ex.extract_LUMO_energy())
print('SCF Done:', ex.extract_SCF())
print('tce', ex.extract_thermal_correction_to_energy())
print('tcenth', ex.extract_thermal_correction_to_enthalpy())
print('tcgfe', ex.extract_thermal_correction_to_gibbs_free_energy())
print('zero-point', ex.extract_zero_point_correction())
print('NPAs', ex.extract_npas())