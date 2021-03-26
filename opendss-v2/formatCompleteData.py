# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:08:47 2019

@author: ylb10119
"""

import pandas as pd
import numpy as np

latLongsRaw =pd.read_csv('tmyResolution.csv', header=None)
latLongs = latLongsRaw.as_matrix()


weatherScotland=np.zeros([420480, 10])

for i in range(1,49):
    tmyProxy = pd.read_csv(r'tmy_data/tmy_'+ str(latLongs[(i-1),1]) + '_'+ str(int(latLongs[(i-1),2])) + '.csv', sep=',', header=None)
    tmy=tmyProxy.iloc[16:,0:]
    tmy.columns=tmy.iloc[0,0:]
    tmy.index=tmy.iloc[0:,0]
    tmy=tmy.drop(tmy.index[[0]])
    tmy=tmy.drop('Date&Time (UTC)', axis=1)
    aprilOn=tmy.iloc[2160:]
    janOn=tmy.iloc[0:2160]
    tmy_data = pd.concat([aprilOn, janOn])
    t=tmy_data.as_matrix()
    if i==1:
        weatherScotland[0:(i*8760),0] = int(latLongs[(i-1),0])
        weatherScotland[0:(i*8760),1:10] = t
    else: 
        weatherScotland[((i-1)*8760):(i*8760),0] = int(latLongs[(i-1),0])
        weatherScotland[((i-1)*8760):(i*8760),1:10] = t
    

ws=pd.DataFrame(weatherScotland)
ws.to_csv('C:/Users/ylb10119/Desktop/weather.csv', index=False, header=False)

# add altitudes 

altitudes=np.zeros(48)
for i in range(0,48):
    tmyProxy = pd.read_csv(r'tmy_data/tmy_'+ str(latLongs[(i),1]) + '_'+ str(int(latLongs[(i),2])) + '.csv', sep=',', header=None)
    altitudes[i]=tmyProxy.iloc[2,1]
    
ll=np.zeros([48,4])
ll[0:,0:3]=latLongs
ll[0:,3]=altitudes
pd.DataFrame(ll).to_csv('C:/Users/ylb10119/Desktop/latLon.csv',index=False, header=False)