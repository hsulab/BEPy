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
        angle_assemble_CMO_ts = dirtool.walk_dir_cal_bond_angle_dic(r'./database/CMO_ts')
        df_CMO_ts=pd.DataFrame(angle_assemble_CMO_ts).T
        angle_assemble_CMO_fs = dirtool.walk_dir_cal_bond_angle_dic(r'./database/CMO_fs')
        df_CMO_fs=pd.DataFrame(angle_assemble_CMO_fs).T
        with pd.ExcelWriter(r'./data_in_excel/CMO_ts.xls') as writer:
            df_CMO_ts.to_excel(writer, '0')
        with pd.ExcelWriter(r'./data_in_excel/CMO_fs.xls') as writer:
            df_CMO_fs.to_excel(writer, '0')
        #print(cal.calculate_bond_angle_fiel1file(r'./database/example1.xsd'))
    #except Exception as e:
        #print(r'Something wrong!')  

###
if __name__ == '__main__':
    main()