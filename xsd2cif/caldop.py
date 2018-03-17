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
###
path = './dopIrO2/'
for xsdfile in os.listdir(path):
    print(xsdfile)
    if re.match(r'/w*.xsd', xsdfile):
        workdir = '%s/%s' %(path, xsdfile)
        print(workdir)
        os.mkdir(workdir)
        os.system('cd %s' %(workdir))
        os.system('cp ../%s ./' %(xsdfile))
        os.system('pwd')
###
