#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: autovasp.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 18:36:16 2018
#########################################################################
import os
###
printout = r'./dopIrO2_1_IrIrRu/suf/print-out'
with open(printout, 'r') as f:
    content = f.readlines()
print(content[-1])
finish_flag = ' reached required accuracy - stopping structural energy minimisation\n'
print(finish_flag)
if content[-1] == finish_flag:
    print('Calculation finished!')
else:
    print('fuck')
