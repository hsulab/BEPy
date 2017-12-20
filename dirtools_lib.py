# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:53:09 2017

@author: Alexander
"""
###
import os
import pandas as pd
import calculate_lib as cal
###
def walk_dir_cal_atom_distance(walk_dir_name):
    distance_assemble = []
    file_information = []
    file_list = os.listdir(walk_dir_name) #列出文件夹下所有的目录与文件
    for i in range(0,len(file_list)):
        file_path = os.path.join(walk_dir_name,file_list[i])
        if os.path.isfile(file_path):
            file_information.append(file_list[i])
            file_information.append(cal.calculate_atom_distance(file_path))
            distance_assemble.append(file_information)
            file_information = []
    return distance_assemble

def walk_dir_cal_atom_distance_dic(walk_dir_name):
    distance_assemble = {}
    file_list = os.listdir(walk_dir_name) #列出文件夹下所有的目录与文件
    for i in range(0,len(file_list)):
        file_path = os.path.join(walk_dir_name,file_list[i])
        if os.path.isfile(file_path):
            distance_assemble[file_list[i]] = cal.calculate_atom_distance(file_path)
    return distance_assemble

def walk_dir_cal_bond_angle_dic(walk_dir_name):
    angle_assemble = {}
    file_list = os.listdir(walk_dir_name) #列出文件夹下所有的目录与文件
    for i in range(0,len(file_list)):
        file_path = os.path.join(walk_dir_name,file_list[i])
        if os.path.isfile(file_path):
            angle_assemble[file_list[i]] = \
            cal.calculate_bond_angle_fiel1file(file_path)
    return angle_assemble
            