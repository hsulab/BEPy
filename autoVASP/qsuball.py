#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: qsuball.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 21:28:59 2018
#d########################################################################
#qsub: Maximum number of jobs already in queue for user MSG=total number of current user's jobs exceeds the queue limit: user jyxu@master.cluster, queue bigmem
###
from autoSet import set_VASPsp
##
import os
import sys
import re
###
global qsub_path
global qsub_dirs
qsub_dirs = []
###
if len(sys.argv) == 1:
    qsub_path = r'./'
elif len(sys.argv) == 2:
    qsub_path = sys.argv[1]
else:
    print('argv wrong!')
qsub_path = os.path.abspath(qsub_path)
###
logfile = os.path.abspath(os.path.join(qsub_path, 'qsub_results.xu'))
if os.path.exists(logfile):
    print('qsub_results.xu exists!')
    print('A new qsub_results.xu is created!')
    os.remove(logfile)
else:
    print('Start!')
### qsub_dirs must be abspath.
def get_qsub_dirs(path):
    global qsub_dirs
    path = os.path.abspath(path)
    work_dirs = ['bulk', 'suf', 'ts', 'fs', 'ab']
    vaspfiles = ['INCAR','POSCAR','POTCAR','KPOINTS','vasp.script']
    #print('cur dir:%s' % os.path.abspath(path))
    if os.path.basename(path) in work_dirs:
        if set(vaspfiles) & set(os.listdir(path)) == set(vaspfiles):
            if 'print-out' in os.listdir(path):
                os.system(r'echo %s Already qsub vasp.script! >> %s' %(path, logfile))
            else:
                qsub_dirs.append(path)
        else:
            lackfile = set(vaspfiles) - set(os.listdir(path))
            lackfile = [str(i) for i in lackfile]
            os.system(r'echo %s Lack %s! >> %s' %(path, lackfile, logfile))

    ###
    for filename in os.listdir(path):
        deeper_dir = os.path.join(path, filename)
        if os.path.isdir(deeper_dir):
            get_qsub_dirs(deeper_dir)
###
def qsub_script(path, queue):
    os.chdir(path)
    os.system(r'echo -e "%s in %s    \c" >> %s' %(path, queue, logfile))
    os.system(r'qsub vasp.script >> %s' %(logfile))
    os.chdir(qsub_path)
###
def qsub_all(number):
    for qsub_dir in qsub_dirs:
        vasp_script = os.path.join(qsub_dir, 'vasp.script')
        ### set default
        set_VASPsp(vasp_script, '#PBS -q', 'bigmem', 1)
        ###
        with open(vasp_script, 'r') as f:
            queue = f.readlines()[6]
        if qsub_dirs.index(qsub_dir) < int(number/2):
            qsub_script(qsub_dir, 'bigmem')
        elif int(number/2) < qsub_dirs.index(qsub_dir) <= number:
            set_VASPsp(vasp_script, '#PBS -q', 'normal', 1)
            qsub_script(qsub_dir, 'normal')

get_qsub_dirs(qsub_path)
qsub_all(16)
