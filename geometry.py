#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:56:08 2017
"""
__author__ = 'Jiayan Xu'

import numpy as np
import re
### my own lib
import find_lib as fd

### calculate the angle
    ### example
    #   begin_element = ['E_b', [X1, Y1, Z1]]
    #   end_element = ['E_e', [X1, Y1, Z1]]
    #   bond_vector = ['E_b --> E_e', array([x, y, z])]
    ###
    #   begin_pattern_str = r'\S*_b'
    #   end_pattern_str = r'\S*_e'
###
def calculate_bond_vector(file_name, begin_pattern_str = r'\S*_b', \
                          end_pattern_str = r'\S*_e'):
    atom_position = fd.find_atom_position(file_name)
    lattice_constant = np.array(fd.find_lattice_constant(file_name))
    bond_frac_vector = []
    bond_vector_3x3 = []
    bond_vector = []
    begin_element = []
    end_element = []
    begin_pattern = re.compile(begin_pattern_str)
    end_pattern = re.compile(end_pattern_str)
    for i in range(len(atom_position)):
        match_begin_element = begin_pattern.search(atom_position[i][0])
        match_end_element = end_pattern.search(atom_position[i][0])
        if match_begin_element:
            begin_element.append(atom_position[i][0])
            begin_element.append(atom_position[i][1])
        #else:
        #    print(str(file_name))
        #    print(r'There is no begin element!')
        if match_end_element:
            end_element.append(atom_position[i][0])
            end_element.append(atom_position[i][1])
        #else:
        #    print(str(file_name))
        #    print(r'There is no end element!')
    
    for i in range(len(begin_element[1])):
        bond_frac_vector.append(begin_element[1][i] - end_element[1][i])
    for i in range(len(lattice_constant)):
        bond_vector_3x3.append(np.array(lattice_constant[i]) * np.array(bond_frac_vector[i]))
    bond_vector.append(str(begin_element[0]) + r' --> ' + str(end_element[0]))
    bond_vector.append(bond_vector_3x3[0]+bond_vector_3x3[1]+bond_vector_3x3[2])
    return bond_vector

###
def calculate_bond_angle_fiel1file(file_name):
    bond_angle = []
    bond1_vector = calculate_bond_vector(file_name, r'\S*_b', r'\S*_e1')
    bond2_vector = calculate_bond_vector(file_name, r'\S*_b', r'\S*_e2')
    bond1_name = bond1_vector[0].split()
    bond2_name = bond2_vector[0].split()
    angle_name = bond1_name[2] + r' <-- ' + bond1_name[0] + r' --> ' \
                + bond2_name[2]
    bond_angle.append(angle_name)
    bond_dotproduct = np.sum(bond1_vector[1]*bond2_vector[1])
    bond_modules_product = np.sqrt(np.sum(bond1_vector[1]**2)) \
                            *np.sqrt(np.sum(bond2_vector[1]**2))
    angle = np.arccos(bond_dotproduct / bond_modules_product)
    bond_angle.append(angle)
    bond_angle.append(str(angle/np.pi*180) + r'°')
    return bond_angle
### calculate the angle
    ### example
    ''' bond_angle = ['angel_name', arc, angle]
    '''
    ###
###

def calculate_bond_angle_from2file(file1_name, file2_name):
    bond_angle = []
    bond1_vector = calculate_bond_vector(file1_name)
    bond2_vector = calculate_bond_vector(file2_name)
    bond1_name = bond1_vector[0].split()
    bond2_name = bond2_vector[0].split()
    angle_name = bond1_name[2] + r'_file1 <-- ' + bond1_name[0] + r'_file1 --> ' \
                + bond2_name[2] + r'_file2'
    bond_angle.append(angle_name)
    bond_dotproduct = np.sum(bond1_vector[1]*bond2_vector[1])
    bond_modules_product = np.sqrt(np.sum(bond1_vector[1]**2)) \
                            *np.sqrt(np.sum(bond2_vector[1]**2))
    angle = np.arccos(bond_dotproduct / bond_modules_product)
    bond_angle.append(angle)
    bond_angle.append(str(angle/np.pi*180) + r'°')
    return bond_angle

###
def calculate_atom_distance(file_name):
    atom_distance = []
    bond_vector = calculate_bond_vector(file_name)
    atom_distance.append(bond_vector[0])
    atom_distance.append(np.sqrt(np.sum(np.array(bond_vector[1])**2)))
    return atom_distance
###
def main():
    print(calculate_bond_vector(r'./database/example1.xsd', r'\S*_b', r'\S*_e1'))
###
if __name__ == "__main__":
    main()
