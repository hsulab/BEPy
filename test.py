# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:05:50 2017

@author: Alexander
"""
### my own lib
import find_lib as fd      
import geometry as cal
import dirtools_lib as dirtool
###
import pandas as pd
### test func
def test():
    file1_name=r'./database/example1.xsd'
    file2_name=r'./database/example2.xsd'
    file3_name=r'./database/example3.xsd'
    atom_position = fd.find_atom_position(file1_name)
    lattice_constant = fd.find_lattice_constant(file1_name)
    ###
    distance_assemble_MO = dirtool.walk_dir_cal_atom_distance_dic(r'./database/OH_ab')
    df_MO=pd.DataFrame(distance_assemble_MO).T
    distance_assemble_CH = dirtool.walk_dir_cal_atom_distance_dic(r'./database/CH')
    df_CH=pd.DataFrame(distance_assemble_CH).T
    ###
    with pd.ExcelWriter(r'./data_in_excel/OH_ab.xls') as writer:
        df_MO.to_excel(writer, '0')
    with pd.ExcelWriter(r'./data_in_excel/CH.xls') as writer:
        df_CH.to_excel(writer, '0')
    print()
        
###
test()