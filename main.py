# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:23:00 2017

@author: Alexander
"""
#!/usr/bin/env python3
# import libs
import sys
import os
import pandas as pd
### my own lib
import find_lib as fd      
import geometry
import dirtools_lib as dirtool
# main func
def main():
    #try:
        angle_assemble_HOM_ab = dirtool.walk_dir_cal_bond_angle_dic(r'./database/HOM_ab')
        df_HOM_ab=pd.DataFrame(angle_assemble_HOM_ab).T
        with pd.ExcelWriter(r'./data_in_excel/HOM_ab.xls') as writer:
            df_HOM_ab.to_excel(writer, '0')
        ###
        angle_assemble_HOM_ts = dirtool.walk_dir_cal_bond_angle_dic(r'./database/HOM_ts')
        df_HOM_ts=pd.DataFrame(angle_assemble_HOM_ts).T
        with pd.ExcelWriter(r'./data_in_excel/HOM_ts.xls') as writer:
            df_HOM_ts.to_excel(writer, '0')
        ###
        angle_assemble_HOM_fs = dirtool.walk_dir_cal_bond_angle_dic(r'./database/HOM_fs')
        df_HOM_fs=pd.DataFrame(angle_assemble_HOM_fs).T
        with pd.ExcelWriter(r'./data_in_excel/HOM_fs.xls') as writer:
            df_HOM_fs.to_excel(writer, '0')
        #print(cal.calculate_bond_angle_fiel1file(r'./database/example1.xsd'))
    #except Exception as e:
        #print(r'Something wrong!')  

###
if __name__ == '__main__':
    main()
