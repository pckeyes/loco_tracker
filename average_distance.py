# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 11:14:46 2017

@author: pckeyes
"""

import pandas as pd
import math
import os
import glob
from itertools import combinations

#get user input
path = raw_input('Enter path containing data to be analyzed: ')
#n_files = int(raw_input('Enter # files to analyze: '))


#get all centroid coordinates files
files = glob.glob(os.path.join(path, 'Centroid_coordinates*.csv'))
dfs = []
n_objects = []
for i in range(0, len(files)):
    dfs.append(pd.read_csv(files[i]))
    n_objects.append(i+1)

#get all combinations of objects to be compared
combos = list(combinations(n_objects,2))
   
#calculate average distance between each pair of objects
for i in range(0, len(combos)):
    total_distance = 0
    n_frames = len(dfs[0].index)
    object_1, object_2 = combos[i] 
    df_1 = dfs[object_1-1]
    df_2 = dfs[object_2-1] 
    for i in range(0, n_frames):
        x_1, y_1 = df_1.iloc[i]
        x_2, y_2 = df_2.iloc[i]
        distance = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
        total_distance += distance
    mean_distance = total_distance/n_frames
    print("Mean distance between objects %i and %i is %.3f" %(object_1, object_2, mean_distance))
