#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: qsuball.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 21:28:59 2018
#d########################################################################
#qsub: Maximum number of jobs already in queue for user MSG=total number of current user's jobs exceeds the queue limit: user jyxu@master.cluster, queue bigmem
##
import os
import sys
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
    os.remove(logfile)
else:
    print('Start!')

def find_dir(string, path='..'):
    global qsub_dirs
    path = os.path.abspath(path)
    vaspfiles = ['INCAR','POSCAR','POTCAR','KPOINTS','vasp.script']
    #print('cur dir:%s' % os.path.abspath(path))
    if set(vaspfiles) & set(os.listdir(path)) == set(vaspfiles):
        if string in os.listdir(path):
            os.system(r'echo %s Already qsub vasp.script! >> %s' %(path, logfile))
        else:
            qsub_dirs.append(path)
    ###
    for filename in os.listdir(path):
        deeper_dir = os.path.join(path, filename)
        if os.path.isdir(deeper_dir):
            find_dir(string, deeper_dir)
###
def qsub_all(number):
    if len(qsub_dirs) >= number:
        for i in range(number):
            path = qsub_dirs[i]
            os.chdir(path)
            os.system('echo "%s     \c" >> %s' %(path, logfile))
            os.system(r'qsub vasp.script >> %s' %(logfile))
            os.chdir(qsub_path)
    else:
        qsub_all(len(qsub_dirs))
find_dir('print-out', qsub_path)
qsub_all(10)
