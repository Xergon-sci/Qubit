import sys
sys.path.append(".")

from qubit.preprocessing.descriptors import tensorise_coulomb_matrix
import pandas as pd

# import the data
data = pd.read_json(r'C:\Users\Michiel Jacobs\Research\Master Thesis\Experimental-Reactivity-Prediction\data\CNOS.json')
data = data.transpose()
data = data['coulomb_matrix'].values

tensor = tensorise_coulomb_matrix(data[0], negative_dimensions=1, positive_dimension=1)
print(tensor)