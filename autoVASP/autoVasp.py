#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: autoVasp.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 18:36:16 2018
#########################################################################
import os
import shutil
import sys
from autoSet import set_INCAR
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
    result_path = './check_printout.xu'
    if not os.path.exists(result_path):
        print('Start!')
    else:
        print('%s exists!' %(result_path))
        os.system(r'rm %s' %(result_path))
        print('%s is removed!' %(result_path))
    finish_flag = ' reached required accuracy - stopping structural energy minimisation\n'
    finished_dirs = []
    for dir in cal_dirs:
        check_dir = os.path.join(dir, 'suf')
        check_file = os.path.join(check_dir, 'print-out')
        if os.path.exists(check_file):
            with open(check_file, 'r') as f:
                content = f.readlines()
            if content[-1] == finish_flag:
                os.system(r'echo Calculation finished in %s! >> %s' %(check_dir, result_path))
                finished_dirs.append(dir)
            else:
                os.system(r'echo Calculation undone or unconverged in %s! >> %s' %(check_dir, result_path))
        else:
            os.system(r'echo There is no print-out in %s >> %s' %(check_dir, result_path))
    return finished_dirs
###
def create_INCAR(dir, suf_dir, ts_dir):
    suf_INCAR = os.path.join(suf_dir, 'INCAR')
    ts_INCAR = os.path.join(ts_dir, 'INCAR')
    shutil.copyfile(suf_INCAR, ts_INCAR)
    set_INCAR(ts_INCAR, 'SYSTEM', os.path.basename(dir) + '_ts')
    set_INCAR(ts_INCAR, 'IBRION', '1')
###
def create_POSCAR(dir, suf_dir, ts_dir):
    content = []
    shutil.copyfile(os.path.join(suf_dir, 'CONTCAR'), os.path.join(ts_dir, 'POSCAR'))
    with open(os.path.join(ts_dir, 'POSCAR'), 'r') as f:
        content = f.readlines()
    new_content = ''
    for i in range(5):
        new_content += content[i]
    new_content += '{:>5}{:>5}'.format('H', 'C') + str(content[5])
    new_content += '{:>5}{:>5}'.format('4', '1') + str(content[6])
    for line in content[7:9]:
        new_content += line
    new_content += '0.573521486444    0.332890746494    0.542347538452    T   T   T\n \
                    0.583968473201    0.643085208862    0.567518468967    T   T   T\n \
                    0.723722447115    0.386856169075    0.609219236308    T   T   T\n \
                    0.442815428287    0.383751349500    0.612745621226    T   T   T\n \
                    0.578859020373    0.423707074865    0.584519962387    T   T   T\n'
    for line in content[9:58]:
        new_content += line
    with open(os.path.join(ts_dir, 'POSCAR'), 'w') as f:
        f.write(new_content)
###
def create_POTCAR(ts_dir, potdir= '/data/pot/vasp/potpaw_PBE.54'):
    POTCAR = ''
    element_pot_list = []
    with open(os.path.join(ts_dir, 'POSCAR'), 'r') as f:
        elements = f.readlines()[5]
    elements = elements.strip('\n').split(' ')
    elements = [i for i in elements if not i == '']
    print(elements)
    for element in elements:
        element_pot_new = '%s/%s_new/POTCAR' %(potdir, element)
        element_pot = '%s/%s/POTCAR' %(potdir, element)
        if os.path.exists(element_pot_new):
            element_pot_list.append(element_pot_new)
        elif os.path.exists(element_pot):
            element_pot_list.append(element_pot)
        else:
            print('Something wrong in %s: POTCAR.' %(ts_dir))
    for pot in element_pot_list:
        with open(pot, 'r') as f:
            pot_content = f.readlines()
        for line in pot_content:
            POTCAR += line
    with open(os.path.join(ts_dir, 'POTCAR'), 'w') as f:
        f.write(POTCAR)
###
def create_fort188(dir, suf_dir, ts_dir):
    with open(os.path.join(ts_dir, 'fort.188'), 'w') as f:
        f.write('1\n3\n6\n4\n0.04\n2   5     1.45016\n0')
###
###
def prepare_ts(finished_dirs):
    result_path = './prepare_ts.xu'
    if not os.path.exists(result_path):
        print('Start!')
    else:
        print('%s exists!' %(result_path))
        os.system(r'rm %s' %(result_path))
        print('%s is removed!' %(result_path))
    ###
    for dir in finished_dirs:
        suf_dir = os.path.join(dir, 'suf')
        ts_dir = os.path.join(dir, 'ts')
        if os.path.exists(ts_dir):
            if not os.path.exists(os.path.join(ts_dir, 'print-out')):
                shutil.rmtree(ts_dir)
                os.system(r'echo %s rming and making ts >> %s' %(ts_dir, result_path))
                os.mkdir(ts_dir)
                create_INCAR(dir, suf_dir, ts_dir)
                shutil.copyfile(os.path.join(suf_dir, 'KPOINTS'), os.path.join(ts_dir, 'KPOINTS'))
                create_POSCAR(dir, suf_dir, ts_dir)
                create_POTCAR(ts_dir, './potpaw_PBE.54')
                create_fort188(dir, suf_dir, ts_dir)
        else:
            os.system(r'echo %s making ts >> %s' %(ts_dir, result_path))
            os.mkdir(ts_dir)
            create_INCAR(dir, suf_dir, ts_dir)
            shutil.copyfile(os.path.join(suf_dir, 'KPOINTS'), os.path.join(ts_dir, 'KPOINTS'))
            create_POSCAR(dir, suf_dir, ts_dir)
            create_POTCAR(ts_dir, './potpaw_PBE.54')
            create_fort188(dir, suf_dir, ts_dir)

###
##
work_dir = []
if len(sys.argv) == 1:
    work_dir = r'./dopIrO2'
elif len(sys.argv) == 2:
    work_dir = sys.argv[1]
    if not os.path.isdir(work_dir):
        sys.exit()
finished_dirs = check_printout(pre_dirs(work_dir))
prepare_ts(finished_dirs)
