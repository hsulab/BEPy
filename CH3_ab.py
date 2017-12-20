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
def get_atom_neighbours_frac(absite_name, xsdfile_name):
    ### IDs & Names, which is to get neighbours' frac coordinates
    atoms_ID_neighbours = MsXsdfile.get_atomsID_neighboursID(xsdfile_name)
    atoms_ID_Name = MsXsdfile.get_atoms_ID_Name(xsdfile_name)
    atoms_Name_ID = MsXsdfile.get_atoms_Name_ID(xsdfile_name)
    ### Atoms' fracs for calculateing the new coordinates
    atoms_Name_frac = MsXsdfile.get_atoms_Name_frac_coordinate(xsdfile_name)
    ###
    absite_neighbours_frac = []
    ###
    for atom_Name, atom_ID in  atoms_Name_ID.items():
        if re.compile(absite_name).search(atom_Name):
            absite_Name = atom_Name
            absite_ID = atom_ID
            break
    ###
    absite_frac = np.array(atoms_Name_frac[absite_Name])
    print(r'= = = = =')
    print(absite_Name, r'_frac_coordinate --> ', '\n', absite_frac)
    print(r'= = = = =')
    ###
    absite_neighbours_ID = atoms_ID_neighbours[absite_ID]
    for atom_ID in absite_neighbours_ID:
        atom_Name = atoms_ID_Name[atom_ID]
        atom_frac = atoms_Name_frac[atom_Name]
        absite_neighbours_frac.append(atom_frac)
    return absite_neighbours_frac
    
######
H_name = 'H\S*'
absite_name = '\w_ab'
M_eq_name = 'O\d{0,3}_eq' 
O_eqab_name = '\w_eqab'
coor_style = ['sp','sp2','sp3','dsp2','dsp3','sp3d','d2sp3','sp3d2']
######
def H_ab(xsdfile_name, coor_style, distance = 1.0):
    ### lattice_information, which is for adjusting coor_vector to assigned distance
    lattice_constant = MsXsdfile.get_lattice_constant(xsdfile_name)
    
    
    ### Some parameters related to absite
    absite_Name = []
    absite_ID = []
    absite_frac = []
    absite_neighbours_ID = []
    absite_neighbours_frac = []
    ### old & new frac coordinates for absorbate atom
    oldab_frac = []
    newab_frac = []
    ### neighbours' coordinates
    ne1_frac = []
    ne2_frac = []
    ###
    ### coor_style for sp2
    ### This method assumes that coor vector is the mid of the other two directions
    if coor_style == r'sp2':
        
        ###
    #
        ###
        ne1_frac = np.array(absite_neighbours_frac[0])
        ne2_frac = np.array(absite_neighbours_frac[1])
        ###
        coor_vector = 2*absite_frac - ne1_frac - ne2_frac
        distance_transform = distance / \
        np.sqrt(np.sum(MsXsdfile.frac2desc(coor_vector, lattice_constant)**2))
        coor_vector = coor_vector * distance_transform
        ###
        for atom_Name, atom_frac in atoms_Name_frac.items():
            if re.compile(H_name).search(atom_Name):
                oldab_frac = atom_frac
                print(r'H_old_frac_coordinate --> ', '\n', atom_frac)
        old_words = r'XYZ="' + ','.join([str(i) for i in oldab_frac]) + '"'
        newab_frac = np.array(absite_frac) + np.array(coor_vector)
        new_words = r'XYZ="' + ','.join([str(i) for i in newab_frac]) + '"'
        ###
        string_switch.string_switch(xsdfile_name, old_words, new_words, 1)
        ###
        print(old_words)
        print(new_words)
            
            
    return              

def main():
    xsdfile_name = r'GeO2+H_copy.xsd'
    #print(atoms_position(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    #H_ab(xsdfile_name, r'sp2', 1.0)
    #print(lattice_constant(r'./GeO2+H_suf110_2x1x4_2fix.xsd'))
    #calculate_atoms_desc_coordinate(xsdfile_name)
    print(get_atom_neighbours_frac('\w_ab', xsdfile_name))
if __name__ == "__main__":
    main()