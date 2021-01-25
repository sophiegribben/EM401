# -*- coding: utf-8 -*-
"""
covariance matrix
Created on Mon Jan 11 14:38:19 2021

@author: Sam
"""
import numpy as np
import pandas as pd
import os


os.getcwd()  # get current working directory

# Read the downloaded data
df_lcl = pd.read_csv("lcl_clean_widefmt.csv", header=0,index_col=0, parse_dates=True)

df_lcl['DayOfWeek']=df_lcl.index.dayofweek
df_lcl['MonthOfYear']=df_lcl.index.month
df_lcl['HH']=df_lcl.index.hour*2+(df_lcl.index.minute/30)

#initialise arrays

#tensor - dimensions day, meter, hh
tensor = np.zeros((365, 754, 48))
#mean 
mu = np.zeros(48)

#cycle through HH - (hour hour) to fill these
for hh in range(0, 48, 1):
    #get the data for this half hour
    data=df_lcl.loc[(df_lcl['HH'] == hh)]
    #convert to numpy and insert into tensor
    np_data = data.to_numpy()
    tensor[0:, 0:, hh] = np_data
    
    #find the mean - make sure this is meaningful!
    mu[hh]=np.mean([data[col].mean() for col in data.columns], axis=0)   
    
    
#find the covariance between days
#cov[X, X] = np.cov()




#sprofile = np.random.multivariate_normal(mu, cov, 10)