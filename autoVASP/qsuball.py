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

def find_dir(string1, string2, path='..'):
    global qsub_path
    #print('cur dir:%s' % os.path.abspath(path))
    if string1 in os.listdir(os.path.abspath(path)):
        if string2 in os.listdir(os.path.abspath(path)):
            os.system(r'echo %s Already qsub vasp.script! >> %s' %(os.path.abspath(path), logfile))
        else:
            os.chdir(os.path.abspath(path))
            os.system(r'qsub vasp.script >> %s' %(logfile))
            os.system(r'echo %s >> %s' %(os.path.abspath(path), logfile))
            os.chdir(os.path.abspath(qsub_path))
    for filename in os.listdir(os.path.abspath(path)):
        deeper_dir = os.path.join(os.path.abspath(path), filename)
        if os.path.isdir(deeper_dir):
            find_dir(string1, string2, deeper_dir)
###
find_dir('vasp.script', 'print-out', qsub_path)
