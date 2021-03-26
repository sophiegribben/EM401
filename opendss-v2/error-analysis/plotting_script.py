# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 13:18:45 2021

Graphing results script
@author: S. Gribben
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Read the data
df_lcl = pd.read_csv("lcl_feederPower.csv", header=None, index_col=0, parse_dates=True)
df_guassian = pd.read_csv("guassian_feederPower.csv", header=None, index_col=0, parse_dates=True)
df_elexon = pd.read_csv("elexon_feederPower.csv", header=None, index_col=0, parse_dates=True)

#crest also needs compared


#plot the lcl data against the models to see the correlation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.scatter(df_guassian, df_lcl)
ax1.set_title("Guassian Model")
ax1.set_xlabel("Actual load (kW)")
ax1.set_ylabel("Synthesised load (kW)")

ax2.scatter(df_elexon, df_lcl)
ax2.set_title("ELEXON profiles")
ax2.set_xlabel("Actual load (kW)")
ax2.set_ylabel("Synthesised load (kW)")


#plot generated profile against profile class 1 and lcl data
fig2 = plt.figure(figsize=(10, 4))
ax2 = plt.axes()
ax2.plot(df_lcl['2018-01-01':'2018-01-07'], label= "LCL data")
ax2.plot(df_guassian['2018-01-01':'2018-01-07'], label= "generated model")
ax2.plot(df_elexon['2018-01-01':'2018-01-07'], label= "ELEXON profiles")
ax2.set_xlabel("Date")
ax2.set_ylabel("feeder power load (kW)")
ax2.legend()


#hourly boxplots
df_lcl['Hour']=df_lcl.index.hour
df_lcl['DayOfWeek']=df_lcl.index.dayofweek
df_lcl['MonthOfYear']=df_lcl.index.month
df_lcl['2018-01-01':'2018-01-30'].boxplot(column=1, by='Hour', figsize=(9,9))

df_guassian['Hour']=df_guassian.index.hour
df_guassian['DayOfWeek']=df_guassian.index.dayofweek
df_guassian['MonthOfYear']=df_guassian.index.month
df_guassian['2018-01-01':'2018-01-30'].boxplot(column=1, by='Hour', figsize=(9,9))

df_elexon['Hour']=df_elexon.index.hour
df_elexon['DayOfWeek']=df_elexon.index.dayofweek
df_elexon['MonthOfYear']=df_elexon.index.month
df_elexon['2018-01-01':'2018-01-30'].boxplot(column=1, by='Hour', figsize=(9,9))

