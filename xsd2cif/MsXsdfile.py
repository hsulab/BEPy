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
def get_information(xsdfile_name, source, information1, information2):
    xsdtree = ET.parse(xsdfile_name)
    atoms_information = {}
    for atom in xsdtree.iter(source):
        if atom.attrib.get(information1) and atom.attrib.get(information2):
            atoms_information[atom.attrib[information1]] = atom.attrib[information2]
    return atoms_information
###
def get_atoms_Name_ID(xsdfile_name):
    return get_information(xsdfile_name, r'Atom3d', r'Name', r'ID')
###
###
def get_atoms_ID_Name(xsdfile_name):
    return get_information(xsdfile_name, r'Atom3d', r'ID', r'Name')
###
def get_atoms_Name_connections(xsdfile_name):
    return get_information(xsdfile_name, r'Atom3d', r'Name', r'Connections')
###
def get_atoms_ID_connections(xsdfile_name):
    return get_information(xsdfile_name, r'Atom3d', r'ID', r'Connections')
###
def get_bond_ID_connects(xsdfile_name):
    return get_information(xsdfile_name, r'Bond', r'ID', r'Connects')
###
### {atom_ID : atom_IDs}
def get_atomsID_neighboursID(xsdfile_name):
    #atoms_Name_connections = get_atoms_Name_connections(xsdfile_name)
    #atoms_Name_ID = get_atoms_Name_ID(xsdfile_name)
    atoms_ID_connections = get_atoms_ID_connections(xsdfile_name)
    bond_ID_connects = get_bond_ID_connects(xsdfile_name)
    ###
    atoms_neighbours = {}
    ###
    for atom_ID, atom_connections in atoms_ID_connections.items():
        atom_connects = set('')
        for bond_ID, bond_connects in bond_ID_connects.items():
            if bond_ID in atom_connections.split(r','):
                atom_connects.update(bond_connects.split(r','))
        atom_connects = atom_connects - set([atom_ID])
        atoms_neighbours[atom_ID] = list(atom_connects)
    return atoms_neighbours
    
    
    
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
def get_atoms_Name_frac(xsdfile_name):
    xsdtree = ET.parse(xsdfile_name)
    atoms_frac = {}
    for atom in xsdtree.iter(r'Atom3d'):
        if atom.attrib.get(r'XYZ') and atom.attrib.get(r'Name'):
            atoms_frac[atom.attrib[r'Name']] = [ float(i) for i in \
                 atom.attrib[r'XYZ'].split(r',') ]
    return atoms_frac
###
###
def calculate_atoms_desc(xsdfile_name):
    atoms_desc = {}
    atoms_frac = get_atoms_Name_frac(xsdfile_name)
    lattice_constant = get_lattice_constant(xsdfile_name)
    for atom_name, frac_coordinate in atoms_frac.items():
        atom_desc = []
        for i in range(3):
            atom_desc.append(np.array(lattice_constant[i]) * np.array(frac_coordinate[i]))
        atoms_desc[atom_name] = \
        atom_desc[0] + atom_desc[1] + atom_desc[2] 
    print(atoms_desc)
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
    #print(get_atoms_ID(xsdfile_name))
    #print(type(get_atoms_connections(xsdfile_name)[r'Ge13']))
    #print(get_bond(xsdfile_name))
    print(get_atoms_ID_neighbours(xsdfile_name))
###
if __name__ == "__main__":
    main()