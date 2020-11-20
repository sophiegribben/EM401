# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:35:08 2020

@author: Sock!
"""
# Import packages
import numpy as np
import pandas as pd

# Update default settings to show 2 decimal place
pd.options.display.float_format = '{:.2f}'.format
# Create a small dataframe
df = pd.DataFrame({'name': ['bob 2012', 'Ava 2013', 'Aby 007', 'XYZ 8', 'GRZ x7', 'Boo VIII', 'Joy 2020'],
                   'p_date': ['2020-02-01', '2020-05-01', '2020-06-30', '2020-04-15', '2020-01-04', '2020-03-21', '2020-07-08'],
                   'count': [80, 30, 10, 60, 40, 20, np.nan],
                   'colour': ['pink', 'teal', 'velvet', 'pink', 'green', 'teal', 'pink'],
                   'radius': [1, 2, 3, 4, 5, 6, 7],
                   'unit': ['cm', 'inch', 'cm', 'cm', 'inch', 'cm', 'cm']})
df

#Create a new coloumn - Radius in cm
df["radius_cm"] = np.where(df['unit']=='inch', 2.54 * df['radius'], df['radius'])

#parse a string - using .str.split
df[['model', 'version']] = df['name'].str.split(' ', expand=True)

#transform datetime variables
# Convert type to datetime
df['p_date'] = pd.to_datetime(df['p_date'])

# Method using .dt.day_name() and dt.year
df['p_dname'] = df['p_date'].dt.day_name()
df['p_year'] = df['p_date'].dt.year