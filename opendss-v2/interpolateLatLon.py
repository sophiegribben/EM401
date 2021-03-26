# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 16:01:58 2019

@author: ylb10119
"""

import pandas as pd
import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import interp1d
import os

def interpolateLatLon(latitude, longitude, t_target, leap, dssDir):
    os.chdir(dssDir)
    latLon = pd.read_csv('latLon.csv', header=None)
    weather = pd.read_csv('weather.csv', header=None)
    diffLatitude=latLon.iloc[0:,1]-latitude
    diffLongitude=latLon.iloc[0:,2]-longitude
    
    latUp=diffLatitude.where(diffLatitude>=0).dropna()
    latDown=diffLatitude.where(diffLatitude<=0).dropna()
    
    lonUp=diffLongitude.where(diffLongitude>=0).dropna()
    lonDown=diffLongitude.where(diffLongitude<=0).dropna()
    
    ##
    
    latUpActual = latUp.where(latUp == latUp[latUp.idxmin()]).dropna()
    latDownActual = latDown.where(latDown == latDown[latDown.idxmax()]).dropna()
    
    lonUpActual = lonUp.where(lonUp == lonUp[lonUp.idxmin()]).dropna()
    lonDownActual = lonDown.where(lonDown == lonDown[lonDown.idxmax()]).dropna()
    
    
    idxLatUp=latUpActual.index
    idxLatDown=latDownActual.index
    idxLonUp=lonUpActual.index
    idxLonDown=lonDownActual.index
    
    idx1 = idxLatDown.intersection(idxLonDown)
    idx2 = idxLatDown.intersection(idxLonUp)
    idx3 = idxLatUp.intersection(idxLonDown)
    idx4 = idxLatUp.intersection(idxLonUp)
    
    lats=list([  latLon.iloc[idx1[0],1],   latLon.iloc[idx2[0],1], latLon.iloc[idx3[0],1], latLon.iloc[idx4[0],1] ])
    lons=list([  latLon.iloc[idx1[0],2],   latLon.iloc[idx2[0],2], latLon.iloc[idx3[0],2], latLon.iloc[idx4[0],2] ])
    
    num=list([  int(latLon.iloc[idx1[0],0]),   int(latLon.iloc[idx2[0],0]), int(latLon.iloc[idx3[0],0]), int(latLon.iloc[idx4[0],0]) ])
    alt=list([  latLon.iloc[idx1[0],3],   latLon.iloc[idx2[0],3], latLon.iloc[idx3[0],3], latLon.iloc[idx4[0],3] ])
    
    pointOneTotal=weather.where(weather.iloc[0:,0]==num[0]).dropna()
    pointTwoTotal=weather.where(weather.iloc[0:,0]==num[1]).dropna()
    pointThreeTotal=weather.where(weather.iloc[0:,0]==num[2]).dropna()
    pointFourTotal=weather.where(weather.iloc[0:,0]==num[3]).dropna()
    
    dS=pd.date_range(start='2015-04-01', end='2016-03-31', freq='H')
    dS1=pd.DataFrame(dS, columns=['Time'])
    pointOneTotal.index= dS1['Time'].iloc[0:8760]
    pointTwoTotal.index= dS1['Time'].iloc[0:8760]
    pointThreeTotal.index=dS1['Time'].iloc[0:8760]
    pointFourTotal.index=dS1['Time'].iloc[0:8760]
    
    pointOne = np.zeros([len(t_target), pointOneTotal.shape[1]])
    pointTwo= np.zeros([len(t_target), pointTwoTotal.shape[1]])
    pointThree = np.zeros([len(t_target), pointThreeTotal.shape[1]])
    pointFour = np.zeros([len(t_target), pointFourTotal.shape[1]])
    
    for i in range(0, len(t_target)):
        pointOne[i,0:] = pointOneTotal[pointOneTotal.index == t_target[i]]
        pointTwo[i,0:] = pointTwoTotal[pointTwoTotal.index == t_target[i]]
        pointThree[i,0:] = pointThreeTotal[pointThreeTotal.index == t_target[i]]
        pointFour[i,0:] = pointFourTotal[pointFourTotal.index == t_target[i]]
        
            
    
    pointWeather = np.zeros([len(pointOne),9])
    for i in range(0,len(pointOne)):
        for k in range(1,10):
            weatherVars = list([pointOne[i,k], pointTwo[i,k], pointThree[i,k], pointFour[i,k]])
            pointWeather[i,(k-1)] = griddata((lats, lons), weatherVars, (latitude, longitude), method='linear')
    
    
    finalData = pd.DataFrame(pointWeather, columns=['DryBulb', 'Humidity','GHI','DNI', 'DHI', 'Infra', 'windS', 'windD','Pressure'] )
    finalData.index = t_target

    
    altitude = griddata((lats, lons), alt, (latitude, longitude), method='linear')
    
    #convert hourly data tp half hourly using interpolation
    hh = np.zeros([finalData.shape[0]*2, 
                                        finalData.shape[1]])
      
    hh[:] = np.NaN
    
    hh[::2, :] = finalData.to_numpy()
    
    hh = hh.astype(float)
    
    hhFinalData = pd.DataFrame(hh)
    
    hhFinalData =hhFinalData.interpolate()    
    
    
    hhRange = pd.date_range(start=str(finalData.iloc[0].name),
                            end=str(finalData.iloc[len(finalData)-1].name + pd.Timedelta(hours=0.5)),
                            freq='30min')
    hhFinalData.index = hhRange
    hhFinalData.columns = finalData.columns
    
    if leap ==1:
        leapH = pd.date_range(start='2/29/2016', end='2/29/2016 23:00:00', freq='H')    
        finalData.drop(leapH, inplace=True)
        leapHH = pd.date_range(start='2/29/2016', end='2/29/2016 23:30:00', freq='0.5H')    
        hhFinalData.drop(leapHH, inplace=True)
    
    
    return finalData, hhFinalData, altitude
