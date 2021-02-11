# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 11:00:46 2021

@author: S. Gribben
"""
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

os.getcwd()  # get current working directory
class1 = pd.read_csv("ProfileClass1.csv", header=0,index_col=0, parse_dates=False)

#extract specific profiles

fig2 = plt.figure()
ax2 = plt.axes()

ax2.plot(class1)#looks rubbish! need to check if its right