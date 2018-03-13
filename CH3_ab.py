# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:43:33 2017

@author: Alexander
"""

### my lib
import string_switch
import MsXsdfile
import get_functional_group as gfg
###
import re
import numpy as np
######
def get_absite_name_neighfrac(xsdfile_name, absite_name_pattern = '\w_s'):
    ### IDs & Names, which is to get neighbours' frac coordinates
    atoms_ID_neighbours = MsXsdfile.get_atomsID_neighboursID(xsdfile_name)
    atoms_ID_Name = MsXsdfile.get_atoms_ID_Name(xsdfile_name)
    atoms_Name_ID = MsXsdfile.get_atoms_Name_ID(xsdfile_name)
    ### Atoms' fracs for calculateing the new coordinates
    atoms_Name_frac = MsXsdfile.get_atoms_Name_frac(xsdfile_name)
    ### absite atom's nenighbours
    absite_name = []
    absite_neighbours_frac = []
    ### get ab site neighbours' fracs
    for atom_Name, atom_ID in  atoms_Name_ID.items():
        if re.compile(absite_name_pattern).search(atom_Name):
            absite_name = atom_Name
            absite_ID = atom_ID
            absite_frac = np.array(atoms_Name_frac[absite_name])
            print(r'= = = = = = = = = =')
            print(absite_name, r'_frac_coordinate --> ', '\n', absite_frac)
            print(r'= = = = = = = = = =')
            ###
            absite_neighbours_ID = atoms_ID_neighbours[absite_ID]
            for atom_ID in absite_neighbours_ID:
                atom_Name = atoms_ID_Name.get(atom_ID, 'No such atom!')
                atom_frac = atoms_Name_frac[atom_Name]
                absite_neighbours_frac.append(atom_frac)
            print(r'= = = = = = = = = =')
            print('absite_neighbours --> ')
            for i in range(len(absite_neighbours_frac)):
                print(i+1, absite_neighbours_frac[i])
            print(r'= = = = = = = = = =')
            ###
            return absite_frac, absite_neighbours_frac
            #break
    else:
        print(r'There is no absorte site atom!')

#####################
def calculate_coor_vector(xsdfile_name, functional_group, ab_name_pattern, \
                          absite_frac, absite_neighbours_frac, distance):
    ### lattice_information, which is for adjusting coor_vector to assigned distance
    lattice_constant = MsXsdfile.get_lattice_constant(xsdfile_name)
    ### get each neighbour's frac
    neigh_frac = np.array(absite_neighbours_frac)
    ### old & new frac coordinates for absorbate atom
    new_frac = []
    ab_atom_name = []
    ab_atom_frac = []
    ###
    coor_vector = np.array([0.0, 0.0, 0.0])
    for i in neigh_frac:
        coor_vector += absite_frac - i
    ### calculate the missing coor direction, adjusting its distance
    distance_transform = distance / \
    np.sqrt(np.sum(MsXsdfile.frac2desc(coor_vector, lattice_constant)**2))
    coor_vector = coor_vector * distance_transform
    ###
    print(r'= = = = = Start = = = = =')
    ### prepare the string switch words
    for group_atom_name, group_atom_old_frac in functional_group.items():
        if re.compile(ab_name_pattern).search(group_atom_name):
            ab_atom_name = group_atom_name
            ab_atom_frac = group_atom_old_frac
            break
    ###
    for group_atom_name, group_atom_old_frac in functional_group.items():
        if re.compile(ab_name_pattern).search(group_atom_name):
            old_words = r'XYZ="' + ','.join([str(i) for i in group_atom_old_frac]) + '"'
            new_frac = np.array(absite_frac) + np.array(coor_vector)
            new_words = r'XYZ="' + ','.join([str(i) for i in new_frac]) + '"'
            string_switch.string_switch(xsdfile_name, old_words, new_words, 1)
            print(r'= = = = = +++++ = = = = =')
            print(group_atom_name)
            print(r'Old position：', old_words)
            print(r'New position：', new_words)
            print(r'= = = = = +++++ = = = = =')
        else:
            old_words = r'XYZ="' + ','.join([str(i) for i in group_atom_old_frac]) + '"'
            new_frac = np.array(absite_frac) + np.array(coor_vector) +\
            np.array(group_atom_old_frac) - np.array(ab_atom_frac)
            new_words = r'XYZ="' + ','.join([str(i) for i in new_frac]) + '"'
            string_switch.string_switch(xsdfile_name, old_words, new_words, 1)
            print(r'= = = = = +++++ = = = = =')
            print(group_atom_name)
            print(r'Old position：', old_words)
            print(r'New position：', new_words)
            print(r'= = = = = +++++ = = = = =')
    print(r'= = = = = Finish = = = = =')
    ###
####################################
######
coor_style = ['sp','sp2','sp3','dsp2','dsp3','sp3d','d2sp3','sp3d2']
######
def ab_move(xsdfile_name, functional_group_pattern, coor_style, distance = 1.0):
    functional_group = \
    gfg.get_functional_group_atoms_frac(xsdfile_name, functional_group_pattern)
    ###
    print(r'xsdfile_name:', xsdfile_name)
    ### Some parameters related to absite
    ab_name_pattern = '\w_ab'
    absite_name_pattern = '\w_s'
    ###s
    (absite_frac, absite_neighbours_frac) = \
    get_absite_name_neighfrac(xsdfile_name, absite_name_pattern)
    ###
    ### coor_style for sp2
    ### This method assumes that coor vector is the mid of the other two directions
    if coor_style == r'sp2':
        if (3 - len(absite_neighbours_frac)) == 1:
            calculate_coor_vector(xsdfile_name, functional_group, ab_name_pattern, \
                                  absite_frac, absite_neighbours_frac, distance)
        else:
            print(r'= = = = = Failed = = = = =')
            print(r'There is', len(absite_neighbours_frac), \
              r'connecting with absite atom')
        ###
        
    if coor_style == r'sp3':
        if (4 - len(absite_neighbours_frac)) == 1:
            calculate_coor_vector(xsdfile_name, functional_group, ab_name_pattern, \
                                  absite_frac, absite_neighbours_frac, distance)
        else:
            print(r'= = = = = Failed = = = = =')
            print(r'There is', len(absite_neighbours_frac), \
              r'connecting with absite atom')
        ###
        
    if coor_style == r'dsp2':
        print(r'f')
    if coor_style == (r'dsp3' or r'sp3d'):
        print(r'f')
    if coor_style == (r'd2sp3' or r'sp3d2s'):
        if (6 - len(absite_neighbours_frac)) == 1:
            calculate_coor_vector(xsdfile_name, functional_group, ab_name_pattern, \
                                  absite_frac, absite_neighbours_frac, distance)
        elif (6 - len(absite_neighbours_frac)) == 2:
            print('haha')
            
        else:
            print(r'= = = = = Failed = = = = =')
            print(r'There is', len(absite_neighbours_frac), \
              r'connecting with absite atom')
        ###
        
def main():
    xsdfile_name = r'OsO2+CH3_suf110_2x1x4_2fix.xsd'
    #prepare_ab(xsdfile_name, '\w_s')
    ab_move(xsdfile_name, r'C1H3', r'd2sp3', 2.0)
    #print(lattice_constant(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    #calculate_atoms_desc_coordinate(xsdfile_name)
    #print(get_atom_neighbours_frac(xsdfile_name, r'H\S*', '\w_ab'))
if __name__ == "__main__":
    main()