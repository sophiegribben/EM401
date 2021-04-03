# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:59:39 2021

Working with the ELEXON data for profile class 1
@author: S. Gribben
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


def generate_week(season):
    #set up for 336 hours (7 days)
    sprofile = np.zeros((1, 336))
    
    #select weekdays -  append for each day
    for i in range(0, 240, 48):
        sprofile[0:, i:(i+48)] = class1_profile(4, season)
        
    #select saturdays
    sprofile[0:, 240:288]=  class1_profile(5, season)
    
    #select sundays
    sprofile[0:, 288:336] = class1_profile(6, season)
    
    #returns the profile with (meters, hours)
    return sprofile

"""
generate year
generates a years worth of data starting on a Monday
inputs: none
outputs: csv file for 300 meters for 1 year

"""
def generate_year():
    #set up array for a years (52 weeks and 1 day) worth of profiles
    year = np.zeros((1, 17520))

    #winter (13 weeks)
    low = 0 
    high = 13 * 336
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Wtr")
    
    #spring (6 weeks)
    low = high
    high = high + (6 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Spr")
        
    #summer (10 weeks)
    low = high
    high = high + (10 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Smr")
    
    #high summer (6 weeks)
    low = high
    high = high + (6 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Hsr")
        
    #autumn (8 weeks)
    low = high
    high = high + (8 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Aut")
        
    #winter (9 weeks + 1 day)
    low = high
    high = high + (9 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Wtr")
    
    #generate a winter monday as the last day
    low = high
    high = high + 48
    year[0:,low:high] = class1_profile(4, "Wtr")
        
    #format into (hours, meters) for the dss model
    #this is currently only for 1 meter!!
    year = np.repeat(year, 300, axis = 0)
    year_dss = year.T

    
    #print into a csv file  
    np.savetxt("elexon_load.csv", year_dss, delimiter=",")
    
    return year_dss  

elexon_load = generate_year()