#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: autoQsub.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 19:45:53 2018
#########################################################################
import re
import sys
###
def alter(file,old_str,new_str):
    #:param file: filename
    #:param old_str: old string
    #:param new_str: new string
    file_data = ""
    with open(file, "r") as f:
        for line in f:
            if re.match(old_str, line):
                line = new_str 
            file_data += line
    with open(file, "w") as f:
        f.write(file_data)
###
if len(sys.argv) == 1:
    INCARfile = r'./dopIrO2_1_IrIrRu/suf/INCAR'
elif len(sys.argv) == 2:
    INCARfile = sys.argv[1]
else:
    print('INCAR file is wrong!')
### IBRION= 2
with open(INCARfile, 'r') as f:
    INCARcontent = f.readlines()
for content in INCARcontent:
    if re.match(r'IBRION=.*', content):
        if not re.match(r'IBRION= 2.*', content):
            alter(INCARfile, 'IBRION', 'IBRION= 2\n')
            print('Set IBRION= 2')
        else:
            print('IBRION=2 Okay!')
        break
