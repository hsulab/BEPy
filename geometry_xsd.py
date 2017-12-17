#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:56:08 2017
"""
__author__ = 'Jiayan Xu'

import numpy as np
import re
### my own lib
import xsdfile as xsd

### calculate the angle
    ### This function return [bond_name, bond_vector]
    ### example
    #   begin_element = {'E_b' ： [X1, Y1, Z1]}
    #   end_element = {'E_e' ： [X1, Y1, Z1]}
    #   bond_name = ['E_b --> E_e']
    #   bond_vector = {'E_b --> E_e' ： array([x, y, z])}
    ###
    #   begin_pattern_str = r'\S*_b'
    #   end_pattern_str = r'\S*_e'
###
def calculate_bond_vector(file_name, begin_pattern_str = r'\S*_b', \
                          end_pattern_str = r'\S*_e'):
    xsdfile = xsd.Xsdfile(file_name)
    atom_position = xsdfile.atoms
    lattice_constant = np.array(xsdfile.cell)
    ###
    bond_frac_vector = []
    bond_vector_3x3 = []
    bond_name = []
    bond_vector = {}
    ###
    begin_atom = []
    end_atom = []
    begin_atom_vector = {}
    end_atom_vector = {}
    ###
    begin_pattern = re.compile(begin_pattern_str)
    end_pattern = re.compile(end_pattern_str)
    for atom in atom_position.keys():
        match_begin_element = begin_pattern.search(atom)
        match_end_element = end_pattern.search(atom)
        if match_begin_element:
            begin_atom = atom
            begin_atom_vector[atom] = atom_position[atom]
        #else:
        #    print(str(file_name))
        #    print(r'There is no begin element!')
        if match_end_element:
            end_atom = atom
            end_atom_vector[atom] = atom_position[atom]
        #else:
        #    print(str(file_name))
        #    print(r'There is no end element!')
    ###
    for i in range(3):
        bond_frac_vector.append(begin_atom_vector[begin_atom][i] - \
                                end_atom_vector[end_atom][i])
    for i in range(3):
        bond_vector_3x3.append(np.array(lattice_constant[i]) * np.array(bond_frac_vector[i]))
    bond_name = begin_atom + r' --> ' + end_atom
    bond_vector[bond_name] = bond_vector_3x3[0]+bond_vector_3x3[1]+bond_vector_3x3[2]
    return [bond_name, bond_vector]
### calculate the angle
    ### example
    ''' bond_angle = ['angle_name', arc, angle]
    '''
    ###
###
def calculate_bond_angle_from1file(file_name):
    ###
    bond_angle = {}
    ###
    bond1 = calculate_bond_vector(file_name, r'\S*_b', r'\S*_e1')
    bond2 = calculate_bond_vector(file_name, r'\S*_b', r'\S*_e2')
    bond1_name = bond1[0]
    bond2_name = bond2[0]
    bond1_vector = bond1[1][bond1_name]
    bond2_vector = bond2[1][bond2_name]
    ###
    angle_name = bond1_name.split()[2] + r' <-- ' + bond1_name.split()[0] + r' --> ' \
                + bond2_name.split()[2]
    ###
    bond_dotproduct = np.sum(bond1_vector*bond2_vector)
    bond_modules_product = np.sqrt(np.sum(bond1_vector**2)) \
                            *np.sqrt(np.sum(bond2_vector**2))
    angle_in_rad = np.arccos(bond_dotproduct / bond_modules_product)
    angle_in_degree = str(angle_in_rad/np.pi*180) + r'°'
    ###
    bond_angle[angle_name] = [angle_in_rad, angle_in_degree]
    return [angle_name, bond_angle]
### calculate the angle
    ### example
    ''' bond_angle = ['angle_name', arc, angle]
    '''
    ###
###
def calculate_bond_angle_from2file(file1_name, file2_name):
    ###
    bond_angle = {}
    ###
    bond1 = calculate_bond_vector(file1_name, r'\S*_b', r'\S*_e1')
    bond2 = calculate_bond_vector(file2_name, r'\S*_b', r'\S*_e2')
    bond1_name = bond1[0]
    bond2_name = bond2[0]
    bond1_vector = bond1[1][bond1_name]
    bond2_vector = bond2[1][bond2_name]
    ###
    angle_name = file1_name +'_'+ bond1_name.split()[2] + r' <-- ' + \
    bond1_name.split()[0] + r' --> ' +'_'+ file2_name + bond2_name.split()[2]
    ###
    bond_dotproduct = np.sum(bond1_vector*bond2_vector)
    bond_modules_product = np.sqrt(np.sum(bond1_vector**2)) \
                            *np.sqrt(np.sum(bond2_vector**2))
    angle_in_rad = np.arccos(bond_dotproduct / bond_modules_product)
    angle_in_degree = str(angle_in_rad/np.pi*180) + r'°'
    ###
    bond_angle[angle_name] = [angle_in_rad, angle_in_degree]
    return [angle_name, bond_angle]

###
def calculate_bond_length(file_name):
    bond_length = {}
    bond_information = calculate_bond_vector(file_name)
    bond_name = bond_information[0]
    bond_length[bond_name] = \
    np.sqrt(np.sum(np.array(bond_information[1][bond_name])**2))
    return [bond_name, bond_length]
###
def main():
    print(calculate_bond_vector(r'./database/example1.xsd', r'\S*_b', r'\S*_e1'))
    print(calculate_bond_length(r'./database/example1.xsd'))
    print(calculate_bond_angle_from1file(r'./database/example1.xsd'))
    print(calculate_bond_angle_from2file(r'./database/example1.xsd',r'./database/example2.xsd'))
###
if __name__ == "__main__":
    main()