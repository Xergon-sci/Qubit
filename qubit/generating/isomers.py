from ..data import bond_nums
import re

def generate_constitutional_isomers(molecular_formula):

    atoms = load_molecular_formula(molecular_formula)
    
    # generate isomers
    # return isomers
    pass

def load_molecular_formula(molecular_formula):
    # validate formula?
    return re.findall(r'([CNOSH])(\d+)?', molecular_formula)