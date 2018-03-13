# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 19:19:16 2017

@author: Alexander
"""
### my lib
import string_switch
import MsXsdfile
###
import re
import numpy as np
######
H_name = 'H\S*'
O_ab_name = 'O\d{0,3}_ab'
O_eq_name = 'O\d{0,3}_eq' 
M_eqab_name = '\w_eqab'
######
def H_ab(xsdfile_name, distance = 1.0):
    atoms_frac_coordinate = MsXsdfile.get_atoms_Name_frac_coordinate(xsdfile_name)
    lattice_constant = MsXsdfile.get_lattice_constant(xsdfile_name)
    ###
    distance_transform = 1.0
    ###
    O_ab_frac_coordinate = []
    O_eq_frac_coordinate = []
    M_eqab_frac_coordinate = []
    ###
    H_old_frac_coordinate = []
    H_new_frac_coordinate = []
    old_words = []
    eq2eqab_frac_vector = []
    new_words = []
    print(r'===== Start Matching =====')
    ###
    for atom, coordinate in atoms_frac_coordinate.items():
        if re.compile(H_name).search(atom):
            H_old_frac_coordinate = coordinate
            print(r'H_old_frac_coordinate --> ', atom, '\n', coordinate)
        if re.compile(O_ab_name).search(atom):
            O_ab_frac_coordinate = coordinate
            print(r'O_ab_frac_coordinate --> ', atom, '\n', coordinate)
        if re.compile(O_eq_name).search(atom):
            O_eq_frac_coordinate = coordinate
            print(r'O_eq_frac_coordinate --> ', atom, '\n', coordinate)
        if re.compile(M_eqab_name).search(atom):
            M_eqab_frac_coordinate = coordinate
            print(r'M_eqab_frac_coordinate --> ', atom, '\n', coordinate)
    print(r'===== Finish Matching =====')
    ###
    old_words = r'XYZ="' + ','.join([str(i) for i in H_old_frac_coordinate]) + '"'
    ###
    print(r'===== Start Calculating =====')
    eq2eqab_frac_vector = np.array(M_eqab_frac_coordinate) - np.array(O_eq_frac_coordinate)
    distance_transform = distance / \
    np.sqrt(np.sum(MsXsdfile.frac2desc(eq2eqab_frac_vector, lattice_constant)**2))
    eq2eqab_frac_vector = eq2eqab_frac_vector * distance_transform
    print(r'distance: ', distance, '\nVector is: ', eq2eqab_frac_vector)
    print(r'===== Finish Calculating =====')
    ###
    H_new_frac_coordinate = np.array(O_ab_frac_coordinate) + np.array(eq2eqab_frac_vector)
    new_words = r'XYZ="' + ','.join([str(i) for i in H_new_frac_coordinate]) + '"'
    ###
    string_switch.string_switch(xsdfile_name, old_words, new_words, 1)
    ###
    print('===== Success =====')
    

def main():
    xsdfile_name = r'GeO2+H_suf110_2x1x4_2fix.xsd'
    #print(atoms_position(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    H_ab(xsdfile_name, 1.0)
    #print(lattice_constant(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    #calculate_atoms_desc_coordinate(xsdfile_name)
if __name__ == "__main__":
    main()