# -*- coding: utf-8 -*-
"""
Get start times of REFIT data
Created on Mon Feb 15 14:50:28 2021

@author: S. Gribben
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import glob
import os

# get current working directory
path = os.getcwd()


"""
# Read each households data
all_files = glob.glob(path + "/*.csv")
df_dict = {}

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    df_dict[filename] = df
"""

# get appliance start times
#how to capture multiple start times?
def app_starttimes(app_num):
    house = str(app_num)
    
    on_times = df[df['Appliance'+ house] > 0]
    
    #extract into numpy
    np_on_times = on_times[['Unix', 'Appliance'+ house]].to_numpy()
    
    
    """
    # find the start values
    for i in range(0, len(np_on_times), 1)
        if np_on_times[i+1]-np_on_times[i] > 1
            start_time = 
            
    """
    
    return np_on_times

#read in the house data
house = str(1)
df = pd.read_csv(path + "/Processed_Data_CSV/House_"+ house +".csv", header=0, index_col="Time")

app1_on = app_starttimes(house)

