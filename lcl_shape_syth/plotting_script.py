# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:56:54 2021

@author: S. Gribben
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import guassian_model as mdl
import extract_profile1



# plot produced profiles against ELEXON profile class 1
day = 4
season = "Hsr"
guassian = mdl.generate_day(day, season, 50)
elexon = extract_profile1.class1_profile(day, season)

x = np.arange(48)
fig = plt.figure(figsize=(12, 5))
ax = plt.axes()
plt.style.use('seaborn-whitegrid')

ax.set_xlabel("Half hour of day")
ax.set_ylabel("Synthesised load (kWh)")
ax.plot(x, guassian.T)
ax.plot(x, elexon, label='ELEXON - Wd Winter')
ax.legend()


#plot histogram of month of LCL data (rather than per season)
df_lcl = pd.read_csv("lcl_clean_widefmt.csv", header=0,index_col=0, parse_dates=True)

df_lcl['DayOfWeek']=df_lcl.index.dayofweek
df_lcl['MonthOfYear']=df_lcl.index.month
df_lcl['HH']=df_lcl.index.hour*2+(df_lcl.index.minute/30)


#create numpy array for mean
mu=np.zeros(48)
#create numpy array for variance
sigma=np.zeros((48, 48))
tensor=np.zeros((20, 754, 48))

for hh in range(0,48,1):
    #extract data
    data=df_lcl.loc[(df_lcl['DayOfWeek'] <= 4) & (df_lcl['HH'] == hh) & (df_lcl['MonthOfYear'] == 2)]

    #uses predefined mean function from numpy
    mu[hh]= np.mean([data[col].mean() for col in data.columns], axis=0)
    
    #convert to numpy and insert into tensor
    tensor[0:, 0:, hh] = data.to_numpy()

#collapse down tensor by taking an average over all meters
lcl_aver = np.average(tensor, axis=1)

#make into a dataframe to plot
df_lcl = pd.DataFrame(lcl_aver)


#plot histograms for each HH
df_lcl.hist(figsize=(15, 15))
    





