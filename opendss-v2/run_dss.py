#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:51:05 2020

@author: rory
"""

# %% add packages
import os
import opendssdirect as dss
import pandas as pd
# import datetime
import numpy as np
# import matplotlib.pyplot as plt
from interpolateLatLon import interpolateLatLon
# from scipy.interpolate import griddata
# from scipy.interpolate import interp1d
# import pvlib
from pvPowerOut import pvPowerOut
import random

def run_dss(networkNum, feederNum, pvPer, pRating, latitude, longitude, loadID, leap, timeLoad):

    #directories
    # dssDir = r'/Users/rory/python/opendss'
    dssDir = os.getcwd()
    netDir = dssDir + '/lv-network-models'
    # netDir = r'/Users/rory/python/opendss/lv-network-models'
    # pvDir = r'/Users/rory/python/pvLibPython'
    
    
    
    # %% import load data
    os.chdir(dssDir)
    
    if timeLoad == 1:
        loadAllClean = pd.read_csv('load1.csv', header=None).to_numpy()
        t = pd.date_range(start='7/26/2008', end='8/30/2008 23:30:00', freq='0.5H')
        t_target = pd.date_range(start='7/26/2015', end='8/30/2015 23:30:00', freq='H')
    elif timeLoad == 2: 
        loadAllClean = pd.read_csv('load2.csv', header=None).to_numpy()
        t = pd.date_range(start='9/9/2008', end='12/31/2008 23:30:00', freq='0.5H')
        t_target = pd.date_range(start='9/9/2015', end='12/31/2015 23:30:00', freq='H')
    elif timeLoad == 3: 
        loadAllClean = pd.read_csv('load3.csv', header=None).to_numpy()   
        t = pd.date_range(start='1/3/2009', end='27/3/2009 23:30:00', freq='0.5H')
        t_target = pd.date_range(start='1/3/2016', end='27/3/2016 23:30:00', freq='H')
    elif timeLoad == 4:   
        loadAllClean = pd.read_csv('load4.csv', header=None).to_numpy()   
        t = pd.date_range(start='4/1/2009', end='5/14/2009 23:30:00', freq='0.5H')
        t_target = pd.date_range(start='4/1/2015', end='5/14/2015 23:30:00', freq='H')
    elif timeLoad == 5:
        loadAllClean = pd.read_csv('load5.csv', header=None).to_numpy()   
        t = pd.date_range(start='5/16/2009', end='7/5/2009 23:30:00', freq='0.5H')
        t_target = pd.date_range(start='5/16/2015', end='7/5/2015 23:30:00', freq='H')
        
    load_all = pd.DataFrame(loadAllClean, index=t)
    
    # %%compile circuit
    os.chdir(netDir + r'/network_' + 
            str(networkNum) + r'/Feeder_'+ str(feederNum))
    
    dss.Basic.DataPath(netDir + r'/network_' + 
            str(networkNum) + r'/Feeder_'+ str(feederNum))
    
    dss.run_command('clear')
    dss.run_command('new circuit.main')
    dss.run_command('Redirect Master2.txt')
    dss.run_command('Edit Vsource.Source BasekV=11 pu=1.00  ISC3=1000  ISC1=500') #3000, 2500
    
    
    #add Monitors and meters
    dss.run_command('new monitor.tr_vi element=transformer.tr1 mode=0 terminal=2') #LV Side V and I
    dss.run_command('new monitor.tr_pq element=transformer.tr1 mode=1 terminal=1 ppolar=no') #HV Side P and Q
    dss.run_command('New EnergyMeter.SS1 Element=Transformer.TR1 action=SAVE')
    
    #solve
    dss.run_command('Solve')
    
    #determine number of loads and buses
    num = dss.Loads.Count()
    bus = dss.Circuit.NumBuses()
    
    # %% extract load info from text file
    f = open('Loads.txt', 'r')
    loadInfo = f.readlines()
    f.close()
    
    loadBus = np.zeros(len(loadInfo))
    for i in range(0, len(loadInfo)):
        loadBus[i] = (float((loadInfo[i].split()[3].split('Bus1=')[1])))
    
    # add pv generators to bus numbers and process pv data
    if pvPer > 0:
        pvBus = random.choices(loadBus, k=round(num*(pvPer/100)))
        
        for i in range(0, len(pvBus)):
            dss.run_command('New Generator.PV_' + str(i) 
                            +' Bus1=' + str(float(pvBus[i]-1)) 
                            +' phases=1 kw=3 kV=0.415 pf=1 model=1')
            
        
    
    # %% get pv data
    # os.chdir(pvDir)
    
    finalData, hhFinalData, altitude = interpolateLatLon(latitude = latitude, 
                                                         longitude = longitude,
                                                         t_target = t_target, 
                                                         leap = leap)
    
    p_acs = pvPowerOut(tmy_data = hhFinalData, 
                       latitude = latitude,
                       longitude = longitude,
                       altitude = altitude,
                       pRating = pRating, 
                       surface_azimuth = 180)
    
    pvData = (p_acs.to_numpy())/1000
    
    
    # %% extract load data
    # if isinstance(loadID, int):
        # loadID= np.random.randint(283, size=num)
    # loadID=random.sample(range(0, 283), num)
    
    load = loadAllClean[0:, loadID]
    
    #reset mon
    dss.Monitors.Reset()
    
    #instantiate result arrays
    d=dss.Circuit.AllBusDistances()
    v1=np.zeros([len(load), bus])
    v2=np.zeros([len(load), bus])
    v3=np.zeros([len(load), bus])
    losses = np.zeros([len(load), 2])
    
    for halfhour in range(0, len(load)):
        iLoad = dss.Loads.First()
        ndeL = -1
        
        
        while iLoad > 0:
            ndeL = ndeL + 1
            dss.Loads.kW(load[halfhour, ndeL])
            iLoad = dss.Loads.Next()
        
        if pvPer > 0:
            iGen = dss.Generators.First()
            ndeG = -1
            while iGen > 0:
                ndeG = ndeG + 1
                dss.Generators.kW(pvData[halfhour])
                iGen = dss.Generators.Next()
            
            
        dss.run_command('Solve')
        dss.Monitors.SampleAll()
            
        v1[halfhour, 0:bus]=dss.Circuit.AllNodeVmagByPhase(1)
        v2[halfhour, 0:bus]=dss.Circuit.AllNodeVmagByPhase(2)
        v3[halfhour, 0:bus]=dss.Circuit.AllNodeVmagByPhase(3)
        
        losses[halfhour,0:] = dss.Circuit.LineLosses()
     
    os.chdir(netDir + r'/network_' + 
            str(networkNum) + r'/Feeder_'+ str(feederNum))    
    #Export Monitors
    dss.run_command('export mon tr_pq')
    dss.run_command('export mon tr_vi')
    
    pq = pd.read_csv('main_Mon_tr_pq.csv')
    vi = pd.read_csv('main_Mon_tr_vi.csv')
    
    #extract data from simulations  
    phase1 = np.zeros([len(load), 4])
    phase1[0:,0] = np.amax(v1[0:,1:], axis=1)
    phase1[0:,1] = pq[' P1 (kW)'].to_numpy()
    phase1[0:,2] = pq[' Q1 (kvar)'].to_numpy()
    phase1[0:,3] = vi[' VAngle1'].to_numpy()
    
    phase2 = np.zeros([len(load), 4])
    phase2[0:,0] = np.amax(v2[0:,1:], axis=1)
    phase2[0:,1] = pq[' P2 (kW)'].to_numpy()
    phase2[0:,2] = pq[' Q2 (kvar)'].to_numpy()
    phase2[0:,3] = vi[' VAngle2'].to_numpy()

    
    phase3 = np.zeros([len(load), 4])
    phase3[0:,0] = np.amax(v3[0:,1:], axis=1)
    phase3[0:,1] = pq[' P3 (kW)'].to_numpy()
    phase3[0:,2] = pq[' Q3 (kvar)'].to_numpy()
    phase3[0:,3] = vi[' VAngle3'].to_numpy()
    
    
    feederMaxVolt = np.zeros([len(load), 1])
    for i in range(0, len(load)):
        feederMaxVolt[i,0] = max(phase1[i,0], phase2[i,0], phase3[i,0])
    
   
    feederPower = np.zeros([len(load), 1])
    feederPower[0:,0] = np.sum([phase1[0:,1], 
                         phase2[0:,1],
                         phase3[0:,1]],
                         axis = 0)
    
    feederReactive = np.zeros([len(load), 1])
    feederReactive[0:,0] = np.sum([phase1[0:,2],
                            phase2[0:,2],
                            phase3[0:,2]],
                            axis = 0)
    
    nodeV = np.zeros([v1.shape[0], load.shape[1]])
    for i in range(0, len(loadBus)):
        nodeV[0:,i] = v1[:,int(loadBus[i])-1]
    
    #delete csv's 
    os.remove('main_Mon_tr_pq.csv')
    os.remove('main_Mon_tr_vi.csv')
    os.remove('MTR_ss1.csv')
     # %%   
    return num, phase1, phase2, phase3, feederMaxVolt, feederPower, feederReactive, nodeV, hhFinalData, loadID, load




