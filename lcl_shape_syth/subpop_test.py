# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 16:42:53 2020

@author: ajp97161
Edited: S. Gribben
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


# get current working directory
os.getcwd()  

# Read the LCL data
df_lcl = pd.read_csv("lcl_clean_widefmt.csv", header=0,index_col=0, parse_dates=True)

df_lcl['DayOfWeek']=df_lcl.index.dayofweek
df_lcl['MonthOfYear']=df_lcl.index.month
df_lcl['HH']=df_lcl.index.hour*2+(df_lcl.index.minute/30)

#read the profile class 1 data
class1 = pd.read_csv("ProfileClass1.csv", header=0,index_col=0, parse_dates=False)

#split up data frame by seasons
#define the seasons from elexons definitions
spring = df_lcl['2013-03-28 00:00:00':'2013-05-14 23:30:00']
summer = df_lcl['2013-05-15 00:00:00':'2013-07-23 23:30:00']
h_summer = df_lcl['2013-07-24 00:00:00':'2013-09-05 23:30:00']
autumn = df_lcl['2013-09-06 00:00:00':'2013-10-30 23:30:00']
winter1 = df_lcl['2013-10-31 00:00:00':'2013-12-31 23:30:00']
winter2 = df_lcl['2013-01-01 00:00:00':'2013-03-27 23:30:00']
winter = pd.concat([winter1, winter2], axis=0)

"""
mean of the elexon profiles
inputs: day (weekday-0, sat-1 or sun-2)
outputs: mean

"""
def class1_mean(day):
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
synth profile
inputs: day (weekday-4, sat-5 or sun-6)
outputs: mean, covariance and 10 guassian profiles

"""
def synth_profile(day, df_season):
    #create numpy array for mean
    mu=np.zeros(48)
    #create numpy array for variance
    sigma=np.zeros((48, 48))

    if day == 4:
        #tensor - dimensions day, meter, hh
        #the number of days depends on the season
        tensor=np.zeros((261, 754, 48))
    else: 
        tensor=np.zeros((52, 754, 48))

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
    lcl_aver = np.transpose(lcl_aver)
    sigma = np.cov(lcl_aver)
    
    #sample from Gaussian distribution:
    sprofile = np.random.multivariate_normal(mu, sigma, 300)
    
    return mu, sigma, sprofile

"""
generate week
generates a weeks worth of data with no specific season attached
inputs: none
outputs: A numpy array of data in the correct format for the dss model 
"""

def generate_week():
    sprofile = np.zeros((300, 336))
    #select weekdays -  append for each day
    for i in range(0, 193, 48):
        mu, sigma, temp_sprofile = synth_profile(4, spring)
        sprofile[0:, i:(i+48)]=temp_sprofile
    
    #select saturdays

    sat_mu, sat_sigma, sat_sprofile = synth_profile(5, spring)
    sprofile[0:, 240:288]=sat_sprofile

    
    #select sundays
    sun_mu, sun_sigma, sun_sprofile = synth_profile(6, spring)
    sprofile[0:, 288:336]=sat_sprofile
    
    #transverse for the 
    return sprofile.T

mu_ave = class1_mean(0)

mu1, sigma1, sprofile1 = synth_profile(5, spring)

    
"""
Save the generated profiles in csv format
week_sprofile = generate_week()
np.savetxt("lcl_load.csv", week_sprofile, delimiter=",")
"""


"""
PLOT GENERATION

#now use Matplotlib to show the mean load profile (with error bars to indicate HH variance)
fig = plt.figure()
ax = plt.axes()
plt.style.use('seaborn-whitegrid')


#arange returns evenly spaced values within a given interval - an array
#up to 48 in this case - a day
x = np.arange(48)
#plot the mean for a day
ax.plot(x, wd_mu)
#add errorbars
plt.errorbar(x, wd_mu, yerr=np.diag(wd_sigma), fmt='.k')

#plot generated profile against profile class 1
fig2 = plt.figure()
ax2 = plt.axes()
#plot the week
ax2.plot(class1_mean(0), label= "Wd average")
ax2.plot(wd_sprofile.T)
ax2.legend()

#create a heatmap of the data for wd, sat, sun 
fig4 = plt.figure()
sns.heatmap(wd_sigma)

fig5 = plt.figure()
sns.heatmap(sat_sigma)

fig6 = plt.figure()
sns.heatmap(sun_sigma)
"""