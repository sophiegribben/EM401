#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 12:00:32 2020

@author: rory
"""

from run_dss_v2 import run_dss_v2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os



networkNum = 1
pvPer = 0#PV percentage...

pRating = 9000
latitude = 56.339 
longitude = - 2.809
leap = 0
loadID = 0
timeLoad = 1

feederNum = 3

phase1, phase2, phase3, feederMaxVolt, feederPower, feederReactive, nodeV, tSrs = run_dss_v2(networkNum, feederNum, pvPer, 
                                                                   pRating, latitude, longitude, loadID, leap, timeLoad)

#save feeder power as csv
df_feederPower= pd.DataFrame(feederPower, index=tSrs)
df_feederPower.to_csv(r'lcl_feederPower.csv', header=False)

# #save feederMaxVolt as csv  
df_feederMaxVolt= pd.DataFrame(feederMaxVolt, index=tSrs)
df_feederMaxVolt.to_csv(r'lcl_feederMaxVolt.csv', header=False)

# plt.plot(feederPower)
# plt.show()