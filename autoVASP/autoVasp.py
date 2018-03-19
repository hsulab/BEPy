#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: autoVasp.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 18:36:16 2018
#########################################################################
import os
###
###
def pre_dirs(work_dir):
    work_dir = os.path.abspath(work_dir) 
    dirs = os.listdir(work_dir)
    cal_dirs = []
    for dir in dirs:
        if os.path.isdir(os.path.join(work_dir, dir)):
            cal_dirs.append(os.path.join(work_dir, dir))
    return cal_dirs

###
def check_printout(cal_dirs):
    finish_flag = ' reached required accuracy - stopping structural energy minimisation\n'
    for dir in cal_dirs:
        check_dir = os.path.join(dir, 'suf')
        check_file = os.path.join(check_dir, 'print-out')
        if os.path.exists(check_file):
            with open(check_file, 'r') as f:
                content = f.readlines()
            if content[-1] == finish_flag:
                os.system(r'echo Calculation finished in %s! >> check_printout.xu' %(check_dir))
            else:
                os.system(r'echo Calculation unfinished or unconverged in %s! >> check_printout.xu' %(check_dir))
        else:
            os.system(r'echo There is no print-out in %s >> check_printout.xu' %(check_dir))
###
result_path = './check_printout.xu'
if not os.path.exists(result_path):
    print('Start!')
else:
    print('%s exists!' %(result_path))
    os.system(r'rm %s' %(result_path))
    print('%s is removed!' %(result_path))
##
###
check_printout(pre_dirs('./dopIrO2'))
