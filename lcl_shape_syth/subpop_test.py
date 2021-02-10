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
def synth_profile(day):
    #create numpy array for mean
    mu=np.zeros(48)
    #create numpy array for variance
    sigma=np.zeros((48, 48))

    if day == 4:
        #tensor - dimensions day, meter, hh
        tensor=np.zeros((261, 754, 48))
    else: 
        tensor=np.zeros((52, 754, 48))

    for hh in range(0,48,1):
        #extract data
        if day == 4:
            data=df_lcl.loc[(df_lcl['DayOfWeek'] <= day) & (df_lcl['HH'] == hh)]
        else: 
            data=df_lcl.loc[(df_lcl['DayOfWeek'] == day) & (df_lcl['HH'] == hh)]
 
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
    sprofile = np.random.multivariate_normal(mu, sigma, 10)
    
    return mu, sigma, sprofile


#select weekdays
wd_mu, wd_sigma, wd_sprofile = synth_profile(4)

#select saturdays
sat_mu, sat_sigma, sat_sprofile = synth_profile(5)

#select sundays
sun_mu, sun_sigma, sun_sprofile = synth_profile(6)

mu_ave = class1_mean(0)

"""
PLOT GENERATION
"""
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
