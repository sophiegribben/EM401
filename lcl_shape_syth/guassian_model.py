# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 16:48:58 2021

Generate a year worth of load profiles 
@author: S. Gribben
"""
import numpy as np
import pandas as pd
import os


# get current working directory
os.getcwd()  

# Read the LCL data
df_lcl = pd.read_csv("lcl_clean_widefmt.csv", header=0,index_col=0, parse_dates=True)

df_lcl['DayOfWeek']=df_lcl.index.dayofweek
df_lcl['MonthOfYear']=df_lcl.index.month
df_lcl['HH']=df_lcl.index.hour*2+(df_lcl.index.minute/30)
    

    
"""
generate day
generates specifed number of profiles for a specific day
inputs: day (weekday-4, sat-5 or sun-6), 
        season (spring-Spr, summer-Smr, high summer-Hsr, autumn-Aut, winter-Wtr)
        num_profiles (how many households to generate)
outputs: numpy array of the produced guassian profiles (meter, hour)

"""
def generate_day(day, season, num_profiles):
    #create numpy array for mean
    mu=np.zeros(48)
    #create numpy array for variance
    sigma=np.zeros((48, 48))
    
    #split up data frame by seasons
    #define the seasons from elexons definitions
    if season == "Spr":
        df_season = df_lcl['2013-03-31 00:00:00':'2013-05-10 23:30:00']
        wd_num = 30
        sat_num = 5
        sun_num = 6
    elif season == "Smr":
        df_season = df_lcl['2013-05-11 00:00:00':'2013-07-19 23:30:00']
        wd_num = 50
        sat_num = 10
        sun_num = 10
    elif season == "Hsr":
        df_season = df_lcl['2013-07-20 00:00:00':'2013-09-01 23:30:00']
        wd_num = 30
        sat_num = 7
        sun_num = 7
    elif season == "Aut":
        df_season = df_lcl['2013-09-02 00:00:00':'2013-10-27 23:30:00']
        wd_num = 40
        sat_num = 8
        sun_num = 8
    elif season == "Wtr":
        winter1 = df_lcl['2013-10-28 00:00:00':'2013-12-31 23:30:00']
        winter2 = df_lcl['2013-01-01 00:00:00':'2013-03-30 23:30:00']
        df_season = pd.concat([winter1, winter2], axis=0)
        wd_num = 111
        sat_num = 22
        sun_num = 21


    
    if day == 4: #weekday
        #tensor - dimensions day, meter, hh
        #the number of days depends on the season
        tensor=np.zeros((wd_num, 754, 48))
    elif day == 5: #saturday
        tensor=np.zeros((sat_num, 754, 48))
    elif day == 6: #sunday
        tensor=np.zeros((sun_num, 754, 48))

    for hh in range(0,48,1):
        #extract data
        if day == 4:
            data=df_season.loc[(df_season['DayOfWeek'] <= day) & (df_season['HH'] == hh)]
        else: 
            data=df_season.loc[(df_season['DayOfWeek'] == day) & (df_season['HH'] == hh)]
 
        #uses predefined mean function from numpy
        mu[hh]= np.mean([data[col].mean() for col in data.columns], axis=0)
        
        #convert to numpy and insert into tensor
        tensor[0:, 0:, hh] = data.to_numpy()
    
    #collapse down by taking an average over all meters
    lcl_aver = np.average(tensor, axis=1)
    
    #find the covariance between days and HH (48x48 matrix)
    lcl_aver = lcl_aver.T
    sigma = np.cov(lcl_aver)
    
    #sample from Gaussian distribution:
    sprofile = np.random.multivariate_normal(mu, sigma, num_profiles)
    
    return sprofile

"""
generate week
generates a weeks worth of data
inputs: the season, number of profiles to produce
outputs: A numpy array of data in the form (meters, hours)
"""

def generate_week(season, num_profiles):
    #set up for specified meters, 336 hours (7 days)
    sprofile = np.zeros((num_profiles, 336))
    #select weekdays -  append for each day
    for i in range(0, 240, 48):
        sprofile[0:, i:(i+48)] = generate_day(4, season, num_profiles)
    
    #select saturdays
    sprofile[0:, 240:288] = generate_day(5, season, num_profiles)

    #select sundays
    sprofile[0:, 288:336] = generate_day(6, season, num_profiles)

    #returns the profile with (meters, hours)
    return sprofile


"""
generate year
generates a years worth of data starting on a Monday
inputs: number of profiles to produce
outputs: csv file for 300 meters for 1 year
         array of results in the form (hours, meters)

"""
def generate_year(num_profiles):
    #set up array for a years (52 weeks and 1 day) worth of profiles
    year = np.zeros((num_profiles, 17520))

    #winter (13 weeks)
    low = 0 
    high = 13 * 336
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Wtr", num_profiles)
    
    #spring (6 weeks)
    low = high
    high = high + (6 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Spr", num_profiles)
        
    #summer (10 weeks)
    low = high
    high = high + (10 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Smr", num_profiles)
    
    #high summer (6 weeks)
    low = high
    high = high + (6 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Hsr", num_profiles)
        
    #autumn (8 weeks)
    low = high
    high = high + (8 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Aut", num_profiles)
        
    #winter (9 weeks + 1 day)
    low = high
    high = high + (9 * 336)
    for i in range(low, high, 336):
        year[0:, i:(i+336)] = generate_week("Wtr", num_profiles)
    
    #generate a winter monday as the last day
    low = high
    high = high + 48
    year[0:,low:high] = generate_day(4, "Wtr", num_profiles)
        
    #format into (hours, meters) for the dss model
    year_dss = year.T    
    
    #print into a csv file  
    np.savetxt("guassian_load_" + str(num_profiles) +"profiles.csv", year_dss, delimiter=",")
    
    return year_dss   

