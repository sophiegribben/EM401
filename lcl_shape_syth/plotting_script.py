# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:18:45 2021

Graphing results script
@author: S. Gribben
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import guassian_model 
import extract_profile1


day = 4
season = "Spr"
mu, sigma, sprofile = guassian_model.synth_profile(day, season)


#use Matplotlib to show the mean load profile (with error bars to indicate HH variance)
fig = plt.figure()
ax = plt.axes()
plt.style.use('seaborn-whitegrid')


#arrange returns evenly spaced values within a given interval - an array
#up to 48 in this case - a day
x = np.arange(48)
#plot the mean for a day
ax.plot(x, mu)
#add errorbars
plt.errorbar(x, mu, yerr=np.diag(sigma), fmt='.k')

#plot generated profile against profile class 1
fig2 = plt.figure()
ax2 = plt.axes()
#plot the week
ax2.plot(extract_profile1.class1_profile(day, season), label= "ELEXON - blue")
ax2.plot(sprofile.T)
ax2.legend()

#create a heatmap of the data 
fig4 = plt.figure()
sns.heatmap(sigma)

