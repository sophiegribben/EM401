# -*- coding: utf-8 -*-
"""
Get start times of REFIT data
Created on Mon Feb 15 14:50:28 2021

@author: S. Gribben
"""
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import datetime
#import glob
import os

# get appliance start times
def app_starttimes():
    #set up dictionary of start times
    all_start_times = {}
    
    #iterate over number of appliances
    number = len(df.columns)-1
    
    for app_num in range(1, number, 1):
        app_num = str(app_num)
        df_on_times = df[df['Appliance'+ app_num] > 0]
        
        #extract into numpy
        on_times = df_on_times[['Unix', 'Appliance'+ app_num]].to_numpy()
        
        # find the start and end values
        #convert from unix
        datetime_time = datetime.datetime.fromtimestamp(on_times[0, 0])
        #initialise the array
        start_time = [datetime_time]
        
        for i in range(1, len(on_times)-1, 1):
            if on_times[i+1, 1] - on_times[i, 1] > 1:
                #convert from unix
                datetime_time = datetime.datetime.fromtimestamp(on_times[i+1, 0])
                #add to the array
                start_time.append(datetime_time)
        
        #convert to numpy array - speed concerns
        start_time = np.asarray(start_time)
        #add to dictionary
        all_start_times[app_num] = start_time
        
        
    return all_start_times

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

#read in the house data
house = str(1)
df = pd.read_csv(path + "/Processed_Data_CSV/House_"+ house +".csv", header=0, index_col="Time")

#get the appliance data for 1 app. in 1 house
app1_on = app_starttimes()

