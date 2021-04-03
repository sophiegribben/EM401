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
df_crest = pd.read_csv("CREST_feederPower.csv", header=None, index_col=0, parse_dates=True)



#plot the lcl data against the models to see the correlation
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
ax1.scatter(df_guassian, df_lcl)
ax1.set_title("Guassian Model")
ax1.set_xlabel("Actual load (kW)")
ax1.set_ylabel("Synthesised load (kW)")

ax2.scatter(df_elexon, df_lcl)
ax2.set_title("ELEXON profiles")
ax2.set_xlabel("Actual load (kW)")
ax2.set_ylabel("Synthesised load (kW)")

ax3.scatter(df_crest, df_lcl)
ax3.set_title("CREST Model")
ax3.set_xlabel("Actual load (kW)")
ax3.set_ylabel("Synthesised load (kW)")


#plot generated profile against profile class 1 and lcl data
fig2 = plt.figure(figsize=(10, 4))
ax2 = plt.axes()
ax2.plot(df_lcl['2013-01-06':'2013-01-12'].to_numpy().flatten(), label= "LCL data")
ax2.plot(df_guassian['2018-01-01':'2018-01-07'].to_numpy().flatten(), label= "generated model")
ax2.plot(df_elexon['2018-01-01':'2018-01-07'].to_numpy().flatten(), label= "ELEXON profiles")
#ax2.plot(df_crest['2018-05-14':'2018-05-20'].to_numpy().flatten(), label= "CREST model")
ax2.set_title("Feeder Load for a week in January")
ax2.set_xlabel("Half Hour")
ax2.set_ylabel("feeder power load (kW)")
ax2.legend()


# #hourly boxplots
# df_lcl['Hour']=df_lcl.index.hour
# df_lcl.boxplot(column=1, by='Hour', figsize=(9,9))

# df_guassian['Hour']=df_guassian.index.hour
# df_guassian.boxplot(column=1, by='Hour', figsize=(9,9))

# df_elexon['Hour']=df_elexon.index.hour
# df_elexon.boxplot(column=1, by='Hour', figsize=(9,9))

# df_crest['Hour']=df_crest.index.hour
# df_crest.boxplot(column=1, by='Hour', figsize=(9,9))


# #hourly histograms
# df_lcl.hist(column=1, by='Hour', figsize=(12, 12))
# df_guassian.hist(column=1, by='Hour', figsize=(12, 12))
# df_elexon.hist(column=1, by='Hour', figsize=(12, 12))
# df_crest.hist(column=1, by='Hour', figsize=(12, 12))