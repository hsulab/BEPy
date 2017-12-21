# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:43:33 2017

@author: Alexander
"""

### my lib
import string_switch
import MsXsdfile
###
import re
import numpy as np
######
def prepare_ab(xsdfile_name, ab_name_pattern, absite_name):
    ### IDs & Names, which is to get neighbours' frac coordinates
    atoms_ID_neighbours = MsXsdfile.get_atomsID_neighboursID(xsdfile_name)
    atoms_ID_Name = MsXsdfile.get_atoms_ID_Name(xsdfile_name)
    atoms_Name_ID = MsXsdfile.get_atoms_Name_ID(xsdfile_name)
    ### Atoms' fracs for calculateing the new coordinates
    atoms_Name_frac = MsXsdfile.get_atoms_Name_frac_coordinate(xsdfile_name)
    ### absite atom's nenighbours
    absite_neighbours_frac = []
    ### absorte's name $ its frac
    ab_name = []
    oldab_frac = []
    ### get absorte atom's name & frac
    for atom_Name, atom_frac in atoms_Name_frac.items():
            if re.compile(ab_name_pattern).search(atom_Name):
                ab_name = atom_Name
                oldab_frac = atom_frac
    print(r'= = = = = = = = = =')
    if ab_name != []:
        print(ab_name, r'_old_frac_coordinate --> ', '\n', oldab_frac)
    else:
        print(r'There is no absorte atom!')
    print(r'= = = = = = = = = =')
    ### get ab site neighbours' fracs
    for atom_Name, atom_ID in  atoms_Name_ID.items():
        if re.compile(absite_name).search(atom_Name):
            absite_Name = atom_Name
            absite_ID = atom_ID
            break
    ###
    absite_frac = np.array(atoms_Name_frac[absite_Name])
    print(r'= = = = = = = = = =')
    print(absite_Name, r'_frac_coordinate --> ', '\n', absite_frac)
    print(r'= = = = = = = = = =')
    ###
    absite_neighbours_ID = atoms_ID_neighbours[absite_ID]
    for atom_ID in absite_neighbours_ID:
        atom_Name = atoms_ID_Name[atom_ID]
        atom_frac = atoms_Name_frac[atom_Name]
        absite_neighbours_frac.append(atom_frac)
    print(r'= = = = = = = = = =')
    print('absite_neighbours --> ')
    for i in range(len(absite_neighbours_frac)):
        print(i+1, absite_neighbours_frac[i])
    print(r'= = = = = = = = = =')
    ###
    return oldab_frac, absite_frac, absite_neighbours_frac
#####################
def calculate_coor_vector(xsdfile_name, oldab_frac, absite_frac, \
                          absite_neighbours_frac, distance):
    ### lattice_information, which is for adjusting coor_vector to assigned distance
    lattice_constant = MsXsdfile.get_lattice_constant(xsdfile_name)
    ### get each neighbour's frac
    ne_frac = np.array(absite_neighbours_frac)
    ### old & new frac coordinates for absorbate atom
    newab_frac = []
    ###
    coor_vector = np.array([0.0, 0.0, 0.0])
    for i in ne_frac:
        coor_vector += absite_frac - i
    ### calculate the missing coor direction, adjusting its distance
    distance_transform = distance / \
    np.sqrt(np.sum(MsXsdfile.frac2desc(coor_vector, lattice_constant)**2))
    coor_vector = coor_vector * distance_transform
    ### prepare the string switch words
    old_words = r'XYZ="' + ','.join([str(i) for i in oldab_frac]) + '"'
    newab_frac = np.array(absite_frac) + np.array(coor_vector)
    new_words = r'XYZ="' + ','.join([str(i) for i in newab_frac]) + '"'
    ###
    print(r'= = = = = Start = = = = =')
    string_switch.string_switch(xsdfile_name, old_words, new_words, 1)
    print(r'Old position：', old_words)
    print(r'New position：', new_words)
    print(r'= = = = = Finish = = = = =')
    ###
####################################
######
coor_style = ['sp','sp2','sp3','dsp2','dsp3','sp3d','d2sp3','sp3d2']
######
def ab_find(xsdfile_name, ab_atom, coor_style, distance = 1.0):
    ###
    print(r'xsdfile_name:', xsdfile_name)
    ### Some parameters related to absite
    ab_name_pattern = ab_atom + '\S*'
    absite_name = '\w_ab'
    ###s
    (oldab_frac, absite_frac, absite_neighbours_frac) = \
    prepare_ab(xsdfile_name, ab_name_pattern, absite_name)
    ###
    ### coor_style for sp2
    ### This method assumes that coor vector is the mid of the other two directions
    if coor_style == r'sp2':
        if (3 - len(absite_neighbours_frac)) == 1:
            calculate_coor_vector(xsdfile_name, oldab_frac, absite_frac, \
                                  absite_neighbours_frac, distance)
        else:
            print(r'= = = = = Failed = = = = =')
            print(r'There is', len(absite_neighbours_frac), \
              r'connecting with ab atom')
        ###
        
    if coor_style == r'sp3':
        if (4 - len(absite_neighbours_frac)) == 1:
            calculate_coor_vector(xsdfile_name, oldab_frac, absite_frac, \
                                  absite_neighbours_frac, distance)
        else:
            print(r'= = = = = Failed = = = = =')
            print(r'There is', len(absite_neighbours_frac), \
              r'connecting with ab atom')
        ###
        
    if coor_style == r'dsp2':
        print(r'f')
    if coor_style == (r'dsp3' or r'sp3d'):
        print(r'f')
    if coor_style == (r'd2sp3' or r'sp3d2s'):
        if (6 - len(absite_neighbours_frac)) == 1:
            calculate_coor_vector(xsdfile_name, oldab_frac, absite_frac, \
                                  absite_neighbours_frac, distance)
        elif (6 - len(absite_neighbours_frac)) == 2:
            
        else:
            print(r'= = = = = Failed = = = = =')
            print(r'There is', len(absite_neighbours_frac), \
              r'connecting with ab atom')
        ###
        
def main():
    xsdfile_name = r'GeO2+H_copy.xsd'
    #print(atoms_position(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    ab_find(xsdfile_name, r'H', r'd2sp3', 1.0)
    #print(lattice_constant(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    #calculate_atoms_desc_coordinate(xsdfile_name)
    #print(get_atom_neighbours_frac(xsdfile_name, r'H\S*', '\w_ab'))
if __name__ == "__main__":
    main()