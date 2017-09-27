# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:14:46 2017

@author: pckeyes
"""

import numpy as np
import pandas as pd
import math
import decimal

#get user input
n_files = int(raw_input('Enter # files to analyze: '))
dfs = []
for i in range(0, n_files):
    dfs.append(pd.read_csv(raw_input('Enter the full path to the file you would like to analyze: ')))

while True:
    ret = raw_input('Would you like to continue analyzing? [y/n]: ')
    if ret == 'n': break
    if n_files > 2:
        object_1 = int(raw_input('Enter the first file you would like to compare by the order you first specified: '))
        object_1 -= 1
        object_2 = int(raw_input('Enter the second file you would like to compare by the order you first specified: '))
        object_2 -= 1
    else:
        object_1 = 0
        object_2 = 1
    
    #calculate average distance between two objects
    total_distance = 0
    n_frames = len(dfs[0].index)
    df_1 = dfs[object_1]
    df_2 = dfs[object_2] 
    for i in range(0, n_frames):
        x_1, y_1 = df_1.iloc[i]
        x_2, y_2 = df_2.iloc[i]
        distance = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
        total_distance += distance
    mean_distance = decimal.Decimal(total_distance/n_frames)
    print("Mean distance between objects is %.3f" %mean_distance)