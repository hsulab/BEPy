#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: autoSet.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 19:45:53 2018
#########################################################################
import re
import sys
###
if len(sys.argv) == 1:
    INCARfile = r'./dopIrO2/dopIrO2_1_IrIrRu/ts/INCAR'
elif len(sys.argv) == 2:
    INCARfile = sys.argv[1]
else:
    print('INCAR file is wrong!')
###
### IBRION= 2
def set_INCAR(INCAR, para, value, noecho=0):
    count = 0
    new_INCAR = ''
    with open(INCAR, 'r') as f:
        for line in f:
            if re.match(r'^%s.*' %(para), line):
                line = '%s= %s\n' %(para, value)
                count += 1
            new_INCAR += line
    with open(INCAR, 'w') as f:
        f.write(new_INCAR)
    if not noecho != 0:
        if count == 1:
            print('Set %s: %s= %s' %(INCAR, para, value))
        else:
            print('Something wrong with %s: %s.' %(INCAR, para))
###
def set_VASPsp(VASPsp, para, value, noecho=0):
    count = 0
    new_VASPsp = ''
    with open(VASPsp, 'r') as f:
        for line in f:
            if re.match(r'^%s.*' %(para), line):
                line = '%s %s\n' %(para, value)
                count += 1
            new_VASPsp += line
    with open(VASPsp, 'w') as f:
        f.write(new_VASPsp)
    if not noecho != 0:
        if count == 1:
            print('Set %s: %s %s' %(VASPsp, para, value))
        else:
            print('Something wrong with %s: %s.' %(VASPsp, para))

