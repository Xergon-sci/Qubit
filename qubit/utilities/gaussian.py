import os

class Extractor:

    def __init__(self, filepath):
        self.filepath = filepath

    def check_normal_execution(self):
        with open(self.filepath, 'rb') as f:
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR) 
            line = f.readline().decode()
            if 'Normal termination of Gaussian' in line:
                return True
            else:
                return False
    
    def extract_cartesian_coordinates():
        NotImplemented
    
    def extract_HOMO_energy():
        NotImplemented
    
    def extract_LUMO_energy():
        NotImplemented

    def extract(self):
        # check normal termination
        if not self.check_normal_execution():
            raise ValueError('Gaussian did not terminate normal. In: {}'.format(self.filepath))

        # extract gaussian data
