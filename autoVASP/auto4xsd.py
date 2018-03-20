#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: auto4xsd.py
# Author: jyxu
# mail: ahcigar@foxmail.com
# Created Time: 日  3/18 18:51:06 2018
#########################################################################
import os
import re
import sys
###
if len(sys.argv) == 1:
    test_path = 'dopIrO2'
elif len(sys.argv) == 2:
    test_path = sys.argv[1]
else:
    print('argv is wrong!')
    sys.exit()
base_path = os.getcwd()
result_path = './results.xu'
## bulk-suf-ts-fs
if not os.path.exists(result_path):
    print('Start!')
else:
    print('%s exists!' %(result_path))
    os.system(r'rm %s' %(result_path))
    print('%s is removed!' %(result_path))
for xsddir in os.listdir(test_path):
    xsdpath = base_path + '/' + test_path + '/' + xsddir + '/' + 'suf'
    for xsdfile in os.listdir(xsdpath):
        xsdfiles = []
        if re.match(r'\w*.xsd', xsdfile):
            xsdfiles.append(xsdfile)
    if 'INCAR' in os.listdir(xsdpath):
        os.system(r'autoQsub.py %s/INCAR' %(xsdpath))
    else:
        print('Wrong with INCAR!')
    if len(xsdfiles) == 1:
        print('There is %d xsdfiles in %s, named %s' %(len(xsdfiles), xsdpath, xsdfiles))
        os.system(r'echo %s >> results.xu' %(xsdpath))
        os.chdir(xsdpath)
        os.system(r'xsd2pos %s >> xsd2pos_config.xu' %(xsdfiles[0]))
        os.chdir(base_path)
    elif len(xsdfiles) == 0:
        os.system(r'echo There is no xsdfile in %s >> results.xu' %(xsdpath))
    else:
        os.system(r'echo Something wrong in %s' %(xsdpath))
