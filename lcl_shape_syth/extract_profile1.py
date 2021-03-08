# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:59:39 2021

Working with the ELEXON data for profile class 1
@author: Sam
"""
import numpy as np
import pandas as pd
import os

os.getcwd()

#read the profile class 1 data
class1 = pd.read_csv("ProfileClass1.csv", header=0,index_col=0, parse_dates=False)
    
"""
mean of the elexon profiles
inputs: day (weekday-4, sat-5 or sun-6)
outputs: mean

"""
def class1_mean(day):
    day = day - 4
    #create numpy array for mean
    mu=np.zeros(48)
    data=np.zeros((48,5))
    
    for hh in range(0,48,1):
        class1_slice=class1.iloc[:, [day, day+3, day+6, day+9, day+12]]
        data=class1_slice.to_numpy()
        #Spitting out the same mean for each column - fix!
        mu[hh]= np.mean(data[hh, 0:])

    return mu

"""
extract ELEXON data
inputs: day, season
outputs: the specific profile
"""
def class1_profile(day, season):
    #turn day into text
    if day == 4:
        day_str = "Wd"
    elif day == 5:
        day_str = "Sat"
    elif day == 6:
        day_str = "Sun"
    
    profile = class1[season + " " + day_str]
    return profile
