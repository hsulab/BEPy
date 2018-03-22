#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: check2dop.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 四  3/22 17:10:34 2018
#########################################################################
import os 
import re
import shutil
###
dop_dirs = os.listdir('./dopIrO2')
dop_dirs = [ os.path.abspath(os.path.join('./dopIrO2', i)) for i in dop_dirs]
dop2dir = []
for dop_dir in dop_dirs:
    dir_name = os.path.basename(dop_dir).split('_')[2]
    print(dir_name)
    dop_elements = re.findall(r'.{2}', dir_name)
    for element in dop_elements:
        if element == 'Ir':
            dop_elements.remove(element)
    if len(set(dop_elements)) <= 2:
        dop2dir.append(dop_dir)
###
for dopdir in dop2dir:
    new_dir = os.path.join(r'./dopIrO2_2', os.path.split(dopdir)[1])
    if not os.path.exists(new_dir):
        shutil.copytree(dopdir, new_dir)
    else:
        shutil.rmtree(new_dir)
        shutil.copytree(dopdir, new_dir)
