# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 17:36:41 2017

@author: Alexander
"""
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
import numpy as np
### dict {atom_name : atom_ID}
def get_atoms_information(xsdfile_name, information):
    xsdtree = ET.parse(xsdfile_name)
    atoms_information = {}
    for atom in xsdtree.iter(r'Atom3d'):
        if atom.attrib.get(r'Name') and atom.attrib.get(information):
            atoms_information[atom.attrib[r'Name']] = atom.attrib[information]
    return atoms_information
###
def get_atoms_ID(xsdfile_name):
    return get_atoms_information(xsdfile_name, r'ID')
###
def get_atoms_connections(xsdfile_name):
    return get_atoms_information(xsdfile_name, r'Connections')
### list [ AVector, BVector, CVecotr ]
def get_lattice_constant(xsdfile_name):
    xsdtree = ET.parse(xsdfile_name)
    lattice_constant = []
    for lattice in xsdtree.iter(r'SpaceGroup'):
            lattice_constant.append([ float(i) for i in lattice.attrib[r'AVector'].split(r',') ])
            lattice_constant.append([ float(i) for i in lattice.attrib[r'BVector'].split(r',') ])
            lattice_constant.append([ float(i) for i in lattice.attrib[r'CVector'].split(r',') ])
    return lattice_constant
###
### dict {atom_name : atom_frac_coordinate}
def get_atoms_frac_coordinate(xsdfile_name):
    xsdtree = ET.parse(xsdfile_name)
    atoms_frac_coordinate = {}
    for atom in xsdtree.iter(r'Atom3d'):
        if atom.attrib.get(r'XYZ') and atom.attrib.get(r'Name'):
            atoms_frac_coordinate[atom.attrib[r'Name']] = [ float(i) for i in \
                 atom.attrib[r'XYZ'].split(r',') ]
    return atoms_frac_coordinate
###
###
def calculate_atoms_desc_coordinate(xsdfile_name):
    atoms_desc_coordinate = {}
    atoms_frac_coordinate = get_atoms_frac_coordinate(xsdfile_name)
    lattice_constant = get_lattice_constant(xsdfile_name)
    for atom_name, frac_coordinate in atoms_frac_coordinate.items():
        atom_desc_coordinate = []
        for i in range(3):
            atom_desc_coordinate.append(np.array(lattice_constant[i]) * np.array(frac_coordinate[i]))
        atoms_desc_coordinate[atom_name] = \
        atom_desc_coordinate[0] + atom_desc_coordinate[1] + atom_desc_coordinate[2] 
    print(atoms_desc_coordinate)
###
def frac2desc(frac_coordinate, lattice_constant):
    desc_coordinate = []
    frac_coordinate = np.array(frac_coordinate)
    for i in range(3):
        desc_coordinate.append(np.array(lattice_constant[i]) * np.array(frac_coordinate[i]))
    desc_coordinate = desc_coordinate[0] + desc_coordinate[1] + desc_coordinate[2]
    return np.array(desc_coordinate)
###
def main():
    xsdfile_name = r'GeO2+H_suf110_2x1x4_2fix.xsd' 
    print(get_atoms_ID(xsdfile_name))
    print(get_atoms_connections(xsdfile_name))

###
if __name__ == "__main__":
    main()