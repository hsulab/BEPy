#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: xsd2cif.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 二  3/13 10:51:44 2018
#########################################################################
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
import numpy as np
import sys
########################################################################
def atom_info(xsdfile_name, info):
    xsdtree = ET.parse(xsdfile_name)
    atoms_info = [] 
    for atom in xsdtree.iter(r'Atom3d'):
        if atom.attrib.get(info):
            atoms_info.append(atom.attrib.get(info))
    return atoms_info
def lattice_info(xsdfile_name, info):
    xsdtree = ET.parse(xsdfile_name)
    lattice_constant = []
    lattice_groupname = []
    lattice_system = []
    lattice_angle = []
    ###
    for lattice in xsdtree.iter(r'SpaceGroup'):
            lattice_constant.append([ float(i) for i in lattice.attrib[r'AVector'].split(r',') ])
            lattice_constant.append([ float(i) for i in lattice.attrib[r'BVector'].split(r',') ])
            lattice_constant.append([ float(i) for i in lattice.attrib[r'CVector'].split(r',') ])
            lattice_groupname.append(lattice.attrib[r'GroupName'])
            lattice_system.append(lattice.attrib[r'System'].lower())
    def get_angle(x, y):
        return np.arccos(np.dot(np.array(x),np.array(y).T)/(np.linalg.norm(x)*np.linalg.norm(y)))/np.pi*180
    lattice_constant = np.array(lattice_constant)
    lattice_angle = [get_angle(lattice_constant[1],lattice_constant[2]),\
                     get_angle(lattice_constant[0],lattice_constant[2]),\
                     get_angle(lattice_constant[0],lattice_constant[1])]
    ###
    lattice_constant = [np.linalg.norm(i) for i in np.array(lattice_constant)]  
    ###
    if info == r'constant':
        return lattice_constant
    elif info == r'angle':
        return lattice_angle
    elif info == r'groupname':
        return lattice_groupname
    elif info == r'system':
        return lattice_system
    ###
def makecif(xsdfile_name):
    print('%s is converting.' %(xsdfile_name))
    lattice_constant = lattice_info(xsdfile_name, 'constant')
    lattice_angle = lattice_info(xsdfile_name, 'angle')
###
    content = '{:<30}\n{:<30}{:<20}\n' \
            .format('data_script', '_audit_creation_metho', '\'xsd2cif.py\'')
    content += '{:<30}{:.5f}\n{:<30}{:.5f}\n{:<30}{:.5f}\n' \
            .format('_cell_length_a', lattice_constant[0],  \
                    '_cell_length_b', lattice_constant[1],  \
                    '_cell_length_c', lattice_constant[2])
    content += '{:<30}{:.2f}\n{:<30}{:.2f}\n{:<30}{:.2f}\n' \
            .format('_cell_angle_alpha', lattice_angle[0],  \
                    '_cell_angle_beta' , lattice_angle[1],  \
                    '_cell_angle_gamma', lattice_angle[2])
    content += '{:<30}{:<10}\n{:<30}{:<10}\n{:<30}{:<10}\n' \
            .format('_symmetry_space_group_H-M'  , 'P1',    \
                    '_symmetry_Int_Tables_number', '1' ,    \
                    '_symmetry_cell_setting'     , 'triclinic')
    content += 'loop_\n_symmetry_equiv_pos_as_xyz\nx,y,z\nloop_\n'
    content += '_atom_site_label\n_atom_site_type_symbol\n_atom_site_occupancy\n'    
    content += '_atom_site_fract_x\n_atom_site_fract_y\n_atom_site_fract_z\n_atom_site_U_iso_or_equiv\n'
###
    atoms_name = atom_info(xsdfile_name, 'Name')
    atoms_component = atom_info(xsdfile_name, 'Components')
    atoms_xyz = [i.split(',') for i in atom_info(xsdfile_name, 'XYZ')]
    for name, component, xyz in zip(atoms_name, atoms_component, atoms_xyz):
        content += '{:<10}{:<10}{:<10}{:<20}{:<20}{:<20}{:<10}\n' \
                .format(name, component, 1.00000, xyz[0], xyz[1], xyz[2], 0.00000)
    print("Finished")
    return content
def main():
    print('script:%s' %(sys.argv[0]))
    for i in range(1, len(sys.argv)):
        infile = sys.argv[i]
        print('{:<5}{:<20}'.format(i, infile))
        with open('%s.cif' %(infile.split(r'/')[-1].split(r'.')[0]) , 'w') as f:
            f.write(makecif(infile))
if __name__ == "__main__":
    main()
##
