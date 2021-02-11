# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 12:57:14 2021

@author: S. Gribben
"""
import os
import pandas as pd


# move to pyCREST dictionary
os.chdir('../pyCREST')
import pyCREST as cr

#create profiles
cr.create_profiles(n=10,daytype='weekend',month=1) 

#extract occupancy profiles
df_crest = pd.read_table("Occfile_2x_month-1_daytype-weekend.dat", sep="\t")
