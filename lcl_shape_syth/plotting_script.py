# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:56:54 2021

@author: S. Gribben
"""
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import guassian_model as mdl
import extract_profile1

day = mdl.generate_day(4, "Spr", 300)
elexon = extract_profile1.class1_profile(4, "Spr")

x = np.arange(48)
fig = plt.figure(figsize=(12, 5))
ax = plt.axes()
plt.style.use('seaborn-whitegrid')

ax.plot(x, day.T)
ax.plot(x, elexon, label= "ELEXON - blue")
ax.set_title("Generated profiles for Weekday in Spring")
ax.set_xlabel("half hour of day")
ax.set_ylabel("Synthesised load (kWh)")
