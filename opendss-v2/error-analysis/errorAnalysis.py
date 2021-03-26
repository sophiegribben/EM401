# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 13:51:56 2021

@author: S. Gribben
"""
import numpy as np 
import pandas as pd
import os

"""
MAPE calculation
input: the actual value (LCL data) and the predicted (guassian model)
output: the mean absolute percentage error
"""
def mape(actual, pred):
    return np.mean(np.abs((actual - pred) / actual)) * 100

"""
Pearsons correlation coefficent
input: the actual value (LCL data) and the predicted (guassian model)
output: the Pearsons correlation coefficent
"""
def pearsons(actual, pred):
    return np.corrcoef(actual, pred)


# get current working directory
os.getcwd()  


# Read the data
lcl = pd.read_csv("lcl_feederPower.csv", header=None, index_col=0, parse_dates=True)
guassian = pd.read_csv("guassian_feederPower.csv", header=None, index_col=0, parse_dates=True)
elexon = pd.read_csv("elexon_feederPower.csv", header=None, index_col=0, parse_dates=True)

# convert to numpy and flatten to get into a 1D array
lcl = lcl.to_numpy().flatten()
guassian = guassian.to_numpy().flatten()
elexon = elexon.to_numpy().flatten()
#crest = 

guassian_mape = mape(lcl, guassian)
elexon_error = mape(lcl, elexon)

guassian_rho = pearsons(lcl, guassian)
elexon_rho = pearsons(lcl, elexon)