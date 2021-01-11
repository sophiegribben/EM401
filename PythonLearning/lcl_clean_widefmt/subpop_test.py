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
#create numpy array for covariance
cov=np.zeros((7, 48))

#playabout with the order of the loops and values
#cycle through days
for day in range(0,7,1):
   
    #cycle through HH - (hour hour) to fill these
    for hh in range(0,48,1):
        #extracts data for all days in march
        fri6pm=df_lcl.loc[(df_lcl['MonthOfYear'] == 3) & (df_lcl['DayOfWeek'] == day) & (df_lcl['HH'] == hh)]

        #uses predefined mean function from numpy
        mu[hh]=np.mean([fri6pm[col].mean() for col in fri6pm.columns], axis=0)
        
        #uses predefined variance function from numpy
        sigma[hh,hh]=np.var([fri6pm[col].var() for col in fri6pm.columns], axis=0)
        
        #uses predefined covariance function from numpy
        cov[day,hh]=np.cov([fri6pm[col].var() for col in fri6pm.columns], bias=True)

"""
#how to get intra-day covariance??
    
#change shape of data into a cube/tensor with dimensions day/hour/meter
"""


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
ax.plot(x,mu)
#add errorbars
plt.errorbar(x, mu, yerr=np.diag(sigma), fmt='.k')

#how to sample from Gaussian distribution:
sprofile = np.random.multivariate_normal(mu, sigma, 10)

fig2 = plt.figure()
ax2 = plt.axes()

ax2.plot(sprofile.T)#looks rubbish! need to check if its right
#ax2.plot(np.mean(profile,axis=0))

fig3 = plt.figure()
sns.violinplot("DayOfWeek", "N0000", data=df_lcl)
#see https://jakevdp.github.io/PythonDataScienceHandbook/04.14-visualization-with-seaborn.html

fig4 = plt.figure()
sns.violinplot("DayOfWeek", "N0000", data=np.log(df_lcl))#any thoughts?