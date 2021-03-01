# -*- coding: utf-8 -*-
"""
Dump pickle of REFIT data
Created on Mon Feb 15 14:50:28 2021

@author: S. Gribben
"""
import pandas as pd
import glob
import os
import pickle

# get current working directory
path = os.getcwd() + "/Processed_Data_CSV" 

# Read each households data
all_files = glob.glob(path + "/*.csv")
df_dict = {}

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df_dict[filename] = df
    
# can use the pickle library to export this dict as binary file 
with open('allhouse_dict.p', 'ab') as output:  # Note: `ab` appends the data
        pickle.dump(df_dict, output, pickle.HIGHEST_PROTOCOL)
        #this file is 10 GB and still gives Memory error on my machine