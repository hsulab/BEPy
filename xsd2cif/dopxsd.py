#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: dop2cif.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 三  3/14 22:11:23 2018
#########################################################################
import os
import re
try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET
import numpy as np
########################################################################
### for IrO2, Ru Rh Pd Os Pt
def atom_dop(xsdfile_name):
    basecell = 'IrO2'
    dopdir = ('./dop%s' %(basecell))
    elements = ['Ir', 'Ru', 'Rh', 'Pd', 'Os', 'Pt']
    xsdtree = ET.parse(xsdfile_name)
    count = 0
    ###
    if not os.path.exists(dopdir):
        os.mkdir(dopdir)
        print(r'Dir is created!')
    else:
        print(r'The dir exists!')
    ###
    for atom in xsdtree.iter(r'Atom3d'):
        name = atom.attrib.get('Name')
        if name:
            if re.match(r'\w*_s1', name):
                atom_s1 = atom
            if re.match(r'\w*_s2', name):
                atom_s2 = atom
            if re.match(r'\w*_s3', name):
                atom_s3 = atom
    ###
    for element_s1 in elements:
        atom_s1.set('Components', element_s1)
        for element_s2 in elements:
            atom_s2.set('Components', element_s2)
            for element_s3 in elements:
                atom_s3.set('Components', element_s3)
                xsdtree.write('%s/dop%s_%d_%s%s%s.xsd' %(dopdir, basecell, \
                        count, element_s1, element_s2, element_s3))
                count += 1
    return print('Dop finished!')
## find .xsd
def dop_iter():
    for i in os.listdir():
        if os.path.isfile(i):
            if re.match(r'\w*\.xsd', i):
                print(i)
### IrO2 s1 s2 s3
def main():
    xsdfile = './IrO2_test.xsd'
    print(atom_dop(xsdfile))
###
if __name__ == "__main__" :
    main()
