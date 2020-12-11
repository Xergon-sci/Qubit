import os
import mmap
import re

"""This submodule aims to provide utilities for the gaussian software package.
It will allow the user to quickly write custom interfaces to analyse the output files.
"""

class Extractor:
    """This class supports data extraction from gaussian output files.
    It provides functionality to extract all the implemented data at once or custom extraction
    can be set up by using its public methods.
    """

    def __init__(self, filepath, labels=None):
        self.filepath = filepath
        self.labels = labels
        self.normal_executions = 0

        # Initialize
        self.check_normal_execution()
        self.check_frequencies()
        self.label_positions = self._get_label_positions()

    def check_normal_execution(self):
        """Checks for normal execution

        Checks for normal execution of the gaussian output file.
        Use this first when writing custom extraction methods to check the validity of the calculations.

        Returns:
            (bool): Returns True when a calculation has normal execution.
        """
        with open(self.filepath, "r") as f:
            for line in f:
                if 'Normal termination of Gaussian' in line:
                    self.normal_executions += 1
        if self.labels != None:
            if self.normal_executions == len(self.labels)+1:
                return True
            else:
                raise Exception('There are {} Normal terminations, please check this file manually: {}'.format(self.normal_executions, self.filepath))
        else:
            if self.normal_executions == 0:
                raise Exception('There are no normal terminations, please check this file manually: {}'.format(self.filepath))
            elif self.normal_executions == 1:
                return True
            else:
                raise Exception('There are multiple normal terminations, please set the labels when constructing the flagg.')
    
    def check_frequencies(self):
        """Check for negative (imaginary) frequencies.
        
        Returns:
            (bool): Returns True if no negative frequencies are found.

        Raises:
            Exception: Raises when negative frequencies are found.
        """
        with open(self.filepath, 'r') as f:
            imag = False
            for line in f:
                if 'Frequencies -- ' in line:
                    split = line.split()
                    if float(split[2]) < 0:
                        imag = True
                    if float(split[3]) < 0:
                        imag = True
                    if float(split[4]) < 0:
                        imag = True
        
        if imag:
            raise Exception('There are imaginary frequencies, please check this file manually: {}'.format(self.filepath))
        else:
            return True

    def _get_label_positions(self):
        results = []
        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f):
                for l in self.labels:
                    if l in line:
                        results.append([i, l])
        
        for i, n in enumerate(results):
            if n[0] == results[i-1][0]:
                results.remove(results[i-1])
        
        def clean_list():
            for i, n in enumerate(results):
                if n[1] == results[i-1][1]:
                    results.remove(results[i-1])
                    clean_list()
        clean_list()
        return results

    def _extract_geometry(self, file):
        file.readline()
        file.readline()
        file.readline()
        file.readline()
        file.readline()

        atoms = []
        xyz = []
        is_molecule = True
        while is_molecule:
            # read and process the line
            line = file.readline()
            split = line.split()

            # check if is still the molecule
            if len(split) == 1:
                is_molecule = False
            else:
                # process the line
                atoms.append(split[1])
                coords = []
                coords.append(split[3])
                coords.append(split[4])
                coords.append(split[5])
                xyz.append(coords)
        return atoms, xyz

    def extract_optimized_geometry(self):
        """Extracts the optimized geometry

        Extracts the optimized geometry from the gaussian output file.

        Returns:
            (tuple): tuple containing:

                atoms (list) : Atom numbers
                coördinates (list): Cartesian coordinates in a 2D list
        """
        results = []
        with open(self.filepath, 'r') as f:
            for line in f:
                if 'Standard orientation' in line:
                    atoms, xyz = self._extract_geometry(f)
                    results.append([atoms, xyz])
                if self.labels[1] in line:
                    break
        return results[-2]

    def extract_SCF(self):
        vals = []
        results = []
        with open(self.filepath, 'r') as f:
            for i, line in enumerate(f):
                if 'SCF Done' in line:
                    split = line.split()
                    vals.append([i, split[4]])
                    
        for p in self._get_label_positions():
            temp = None
            for v in vals:
                if v[0] < p[0]:
                    temp = v
            temp = [p[1], temp[1]]
            results.append(temp)    
        return results

    def extract_HOMO_energy(self):
        NotImplemented

    def extract_LUMO_energy(self):
        NotImplemented
