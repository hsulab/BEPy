# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 16:35:58 2017

@author: Alexander
"""
import re
#
### find the matched line
def find_line(file_name,re_formula):
    pattern = re.compile(re_formula)
    match_lines=[]
    try:
        with open(file_name, 'r') as file_open:
            lines = file_open.readlines()
            for line in lines:
                if not line:
                    break
                else:
                    if pattern.search(line):
                        match_lines.append(line.strip())
    except Exception as e:
        print(e + '''
              Advice: Check your input file.''')
    return match_lines
### find all atoms' frac positions in the file
    ### exmaple for atom_position
    '''[ ['E1', [X1, Y1, Z1]], 
         ['E2', [X2, Y2, Z2]],
         ....................,
         ['En', [Xn, Yn, Zn]] ]
    '''
    ###
###
def find_atom_position(file_name, atom_name_pattern_str = r'\S*'):
    ###
    atom_position = []
    ###
    try:
        match_lines = find_line(file_name, r'Atom3d')
    except Exception as e:
        print(e)
    ###
    atom_name_pattern = re.compile(r'Name="' + atom_name_pattern_str + r'"')
    atom_xyz_pattern = re.compile(r'XYZ="' + atom_name_pattern_str + r'"')
    ###
    for i in match_lines:
        match_atom_name = atom_name_pattern.search(i)
        match_atom_xyz = atom_xyz_pattern.search(i)
        if match_atom_name:
            element_name = match_atom_name.group().strip(r'Name=').strip(r'"')
        if match_atom_xyz:
            element_xyz = match_atom_xyz.group().strip(r'XYZ=').strip(r'"').split(r',')
            element_xyz = [float(i) for i in element_xyz]
        atom_position.append([element_name,element_xyz])
    return atom_position
### find the cell information in the file
    ### example for cell_information
    '''[ [A1, A2, A3], 
         [B1, B2, B3], 
         [C1, C2, C3] ]
    '''
    ###
###
def find_lattice_constant(file_name):
    lattice_constant = []
    try:
        match_lines = find_line(file_name, r'SpaceGroup')
    except Exception as e:
        print(e)
    vector_pattern_list = [r'(AVector="\S*")',
                           r'(BVector="\S*")',
                           r'(CVector="\S*")']
    for i in match_lines:
        for j in range(len(vector_pattern_list)):
            vector_pattern = re.compile(vector_pattern_list[j])
            match_vector = vector_pattern.search(i)
            if match_vector:
                vector = match_vector.group()[9:-1].split(r',')
                vector = [ float(i) for i in vector]
                lattice_constant.append(vector)
    return lattice_constant