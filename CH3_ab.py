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
H_name = 'H\S*'
M_ab_name = 'O\d{0,3}_ab'
M_eq_name = 'O\d{0,3}_eq' 
O_eqab_name = '\w_eqab'
coor_style = ['sp','sp2','sp3','dsp2','dsp3','sp3d','d2sp3','sp3d2']
######
def H_ab(xsdfile_name, coor_style, distance = 1.0):
    ###
    lattice_constant = MsXsdfile.get_lattice_constant(xsdfile_name)
    atoms_frac_coordinate = MsXsdfile.get_atoms_Name_frac_coordinate(xsdfile_name)
    ###
    atoms_ID_neighbours = MsXsdfile.get_atomsID_neighboursID(xsdfile_name)
    ###
    atoms_ID_Name = MsXsdfile.get_atoms_ID_Name(xsdfile_name)
    atoms_Name_ID = MsXsdfile.get_atoms_Name_ID(xsdfile_name)
    ###
    atoms_Name_frac = MsXsdfile.get_atoms_Name_frac_coordinate(xsdfile_name)
    ###
    M_ab_Name = []
    M_ab_frac = []
    M_ab_ID = []
    M_ab_neighbours_ID = []
    M_ab_neighbours_frac = []
    ###
    ###
    if coor_style == r'sp2':
        for atom_Name, atom_ID in  atoms_Name_ID.items():
            if re.compile(M_ab_name).search(atom_Name):
                M_ab_Name = atom_Name
                M_ab_ID = atom_ID
                break
        ###
        M_ab_frac = np.array(atoms_Name_frac[M_ab_Name])
        print(M_ab_Name, r'_frac_coordinate --> ', '\n', M_ab_frac)
        ###
        M_ab_neighbours_ID = atoms_ID_neighbours[M_ab_ID]
        for atom_ID in M_ab_neighbours_ID:
            atom_Name = atoms_ID_Name[atom_ID]
            atom_frac = atoms_Name_frac[atom_Name]
            M_ab_neighbours_frac.append(atom_frac)
        c1_frac = np.array(M_ab_neighbours_frac[0])
        c2_frac = np.array(M_ab_neighbours_frac[1])
        ###
        vector = 2*M_ab_frac - c1_frac - c2_frac
        distance_transform = distance / np.sqrt(np.sum(MsXsdfile.frac2desc(vector, lattice_constant)**2))
        vector = vector * distance_transform
        ###
        for atom, coordinate in atoms_frac_coordinate.items():
            if re.compile(H_name).search(atom):
                H_old_frac_coordinate = coordinate
                print(r'H_old_frac_coordinate --> ', atom, '\n', coordinate)
        old_words = r'XYZ="' + ','.join([str(i) for i in H_old_frac_coordinate]) + '"'
        new_frac_coordinate = np.array(M_ab_frac) + np.array(vector)
        new_words = r'XYZ="' + ','.join([str(i) for i in new_frac_coordinate]) + '"'
        ###
        string_switch.string_switch(xsdfile_name, old_words, new_words, 1)
        ###
        print(old_words)
        print(new_words)
            
            
    return 

def CH3_ab(coor_style, xsdfile_name,distance = 1.0):
    coor_style(xsdfile_name)         
        

def main():
    xsdfile_name = r'GeO2+H_suf110_2x1x4_2fix.xsd'
    #print(atoms_position(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    H_ab(xsdfile_name, r'sp2', 1.0)
    #print(lattice_constant(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    #calculate_atoms_desc_coordinate(xsdfile_name)
if __name__ == "__main__":
    main()