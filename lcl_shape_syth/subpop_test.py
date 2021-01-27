# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 16:42:53 2020

@author: ajp97161

"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
#statistical data vis library based on matplotlib
import seaborn as sns

os.getcwd()  # get current working directory

# Read the downloaded data
df_lcl = pd.read_csv("lcl_clean_widefmt.csv", header=0,index_col=0, parse_dates=True)

df_lcl['DayOfWeek']=df_lcl.index.dayofweek
df_lcl['MonthOfYear']=df_lcl.index.month
df_lcl['HH']=df_lcl.index.hour*2+(df_lcl.index.minute/30)

#create numpy array for mean
mu=np.zeros(48)
#create numpy array for variance
sigma=np.zeros((48, 48))

#find the mean for Weekdays in March 
for hh in range(0,48,1):
    
    fri6pm=df_lcl.loc[(df_lcl['MonthOfYear'] == 3) & (df_lcl['DayOfWeek'] <= 5) & (df_lcl['HH'] == hh)]
    
    #uses predefined mean function from numpy
    mu[hh]=np.mean([fri6pm[col].mean() for col in fri6pm.columns], axis=0)


"""
covariance calculation

"""
#tensor - dimensions day, meter, hh
tensor = np.zeros((365, 754, 48))

#cycle through HH - (hour hour) to fill these
for hh in range(0, 48, 1):
    #get the data for this half hour
    data=df_lcl.loc[(df_lcl['HH'] == hh)]
    
    #convert to numpy and insert into tensor
    tensor[0:, 0:, hh] = data.to_numpy()
    

#collapse down by taking an average over all meters
lcl_aver = np.average(tensor, axis=1)

 
#find the covariance between days and HH (48x48 matrix)
lcl_aver = np.transpose(lcl_aver)  
sigma=np.cov(lcl_aver)



"""
PLOT GENERATION
"""
#now use Matplotlib to show the mean load profile (with error bars to indicate HH variance)
fig = plt.figure()
ax = plt.axes()

plt.style.use('seaborn-whitegrid')

#how to sample from Gaussian distribution:
sprofile = np.random.multivariate_normal(mu, sigma, 10)


#arange returns evenly spaced values within a given interval - an array
#up to 48 in this case - a day
x = np.arange(48)
#plot the mean for a day
ax.plot(x, mu)
#add errorbars
plt.errorbar(x, mu, yerr=np.diag(sigma), fmt='.k')


fig2 = plt.figure()
ax2 = plt.axes()

ax2.plot(sprofile.T)#looks rubbish! need to check if its right
#ax2.plot(np.mean(profile,axis=0))

fig3 = plt.figure()
sns.violinplot("DayOfWeek", "N0000", data=df_lcl)
#see https://jakevdp.github.io/PythonDataScienceHandbook/04.14-visualization-with-seaborn.html

fig4 = plt.figure()
sns.violinplot("DayOfWeek", "N0000", data=np.log(df_lcl))

#create a heatmap of the data
fig4 = plt.figure()
sns.heatmap(sigma)