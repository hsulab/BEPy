# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 20:01:34 2017

@author: Alexander
"""
###
import MsXsdfile
###
import re
import numpy as np
###
def check_functional_group_input(functional_group):
    print(functional_group)
    functional_group = re.findall(r'[0-9]+|[A-Za-z]+',functional_group)
    group_atoms = {}
    if len(functional_group)%2 == 0:
        for i in range(len(functional_group)):
            if (i%2==0 and functional_group[i].isalpha()) or \
            (i%2==1 and functional_group[i].isdigit()):
                pass
            else:
                return print(r'Wrong Input!!!')
        for i in range(0,len(functional_group),2):
            group_atoms[functional_group[i]] = functional_group[i+1]        
        return group_atoms
    else:
        return print(r'Wrong Input!!!')
###
def get_functional_group_atoms_frac(xsdfile_name, functional_group):
    atoms_name_frac = MsXsdfile.get_atoms_Name_frac(xsdfile_name)
    group_atoms = check_functional_group_input(functional_group)
    group_atoms_name_frac = {}
    for group_atom_name, group_atom_number in group_atoms.items():
        count = 0
        for atom_name, frac in atoms_name_frac.items():
            if count < int(group_atom_number):
                if re.compile(group_atom_name+r'\S*').search(atom_name):
                    group_atoms_name_frac[atom_name] = frac
                    count += 1
                else:
                    pass
            else:
                break
    print(r'= = = = = = = = = =')
    if group_atoms_name_frac != {}:
        for atom_name, atom_frac in group_atoms_name_frac.items():
            print(atom_name, r'-->', '\n', atom_frac)
    else:
        print(r'No group atoms!')
    print(r'= = = = = = = = = =')
    return group_atoms_name_frac
    
def main():
    xsdfile_name = r'GeO2+CH3.xsd'
    functional_group = r'C1H3'
    print(check_functional_group_input(functional_group))
    print(get_functional_group_atoms_frac(xsdfile_name, functional_group))
###
if __name__ == "__main__":
    main()
        