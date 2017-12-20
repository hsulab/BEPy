# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 13:35:40 2017

@author: Alexander
"""
###
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
###
class Atoms(object):
    def __init__(self, xsdfile_name):
        self.file = xsdfile_name
### r'./database/example1.xsd'
class Xsdfile(object):
    def __init__(self, xsdfile_name):
        ###
        self.file = xsdfile_name
        ###
        atoms = {}
        xsdtree = ET.parse(xsdfile_name)
        for atom in xsdtree.iter(r'Atom3d'):
            atoms[atom.attrib[r'Name']] = [ float(i) for i in \
                 atom.attrib[r'XYZ'].split(r',') ]
        self.atoms = atoms
        cell = []
        for lattice in xsdtree.iter(r'SpaceGroup'):
            cell.append([ float(i) for i in lattice.attrib[r'AVector'].split(r',') ])
            cell.append([ float(i) for i in lattice.attrib[r'BVector'].split(r',') ])
            cell.append([ float(i) for i in lattice.attrib[r'CVector'].split(r',') ])
        self.cell = cell
def main():
    xsdfile = Xsdfile(r'./database/example1.xsd')
    for i in xsdfile.atoms.keys():
        print(i)
    print(xsdfile.atoms)
    print(xsdfile.cell)
if __name__ == "__main__":
    main()