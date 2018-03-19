#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: caldop.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 六  3/17 21:10:51 2018
#########################################################################
import os
import re
import sys
import shutil
###
#path = sys.argv[0]
#os.system('cd %s' %(path))
path = './dopIrO2'
for xsdfile in os.listdir(path):
    if re.match(r'\w*.xsd', xsdfile):
        workdir = '%s/%s/suf' %(path, os.path.splitext(xsdfile)[0])
        print(workdir)
        os.makedirs(workdir) 
        shutil.copy('%s/%s' %(path, xsdfile), '%s/' %(workdir))
        os.remove('%s/%s' %(path, xsdfile))
###
