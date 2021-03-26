# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 11:24:53 2021

@author: S. Gribben
"""
import numpy as np

#load the CREST model power file (10 profiles for 24 hrs (1 min resolution))
data = np.loadtxt('Pfile_50x_month-1_daytype-weekday.dat')

HHload = np.zeros((50, 48))

for profile in range(0, 50, 1):
    for i in range(0, 1440, 30):
        HHload[profile, i//30]=(np.sum(data[profile, i:(i+30)], axis=0))/2000


#print into a csv file  
np.savetxt("CRESTmin_load.csv", data.T, delimiter=",")