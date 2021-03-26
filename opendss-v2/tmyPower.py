# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 09:43:09 2019

@author: ylb10119
"""

import os
import inspect

#scientific python add-ons
import numpy as np
import pandas as pd

#plotting stuff
import matplotlib.pyplot as plt
import matplotlib as mpl

#finally, import the pvlib library
import pvlib

##Load TMY Data


# Find the absolute file path to your pvlib installation
pvlib_abspath = os.path.dirname(os.path.abspath(inspect.getfile(pvlib)))

# absolute path to a data file
datapath = os.path.join(pvlib_abspath, 'data', '703165TY.csv')

# read tmy data with year values coerced to a single year
tmy_data, meta = pvlib.tmy.readtmy3(datapath, coerce_year=2015)
tmy_data.index.name = 'Time'


# TMY data seems to be given as hourly data with time stamp at the end
# shift the index 30 Minutes back for calculation of sun positions
tmy_data = tmy_data.shift(freq='-30Min')['2015']


#Look at the imported version of the TMY file
tmy_data.head()

#plot the GHI data from the TMY file
tmy_data['GHI'].plot()
plt.ylabel('Irradiance (W/m**2)')

#Before we can calculate power for all times in the TMY file, we first need to calculate:
    # solar position
    # extra terrestrial radiation
    # airmass
    # angle of incidence
    # POA sky and ground diffuse radiation
    # cell and module temperatures

# First define some PV system parameters
surface_tilt = 30
surface_azimuth = 180 # pvlib uses 0=North, 90=East, 180=South, 270=West convention
albedo = 0.2

# create pvlib Location object based on meta data
sand_point = pvlib.location.Location(meta['latitude'], meta['longitude'], tz='US/Alaska', 
                                     altitude=meta['altitude'], name=meta['Name'].replace('"',''))
print(sand_point)

# SOLAR POSITION
# Calculate the solar position for all times in the TMY file


solpos = pvlib.solarposition.get_solarposition(tmy_data.index, sand_point.latitude, sand_point.longitude)

solpos.plot()

#DNI ET 
#calculate extra terrestrial radiation - this is needed for many plane of array diffuse irradiance models

# the extraradiation function returns a simple numpy array
# instead of a nice pandas series. We will change this
# in a future version
dni_extra = pvlib.irradiance.extraradiation(tmy_data.index)
dni_extra = pd.Series(dni_extra, index=tmy_data.index)

dni_extra.plot()
plt.ylabel('Extra terrestrial radiation (W/m**2)')

#Airmass

airmass = pvlib.atmosphere.relativeairmass(solpos['apparent_zenith'])
airmass.plot()
plt.ylabel('Airmass')

#POA Sky diffuse

poa_sky_diffuse = pvlib.irradiance.haydavies(surface_tilt, surface_azimuth,
                                             tmy_data['DHI'], tmy_data['DNI'], dni_extra,
                                             solpos['apparent_zenith'], solpos['azimuth'])

poa_sky_diffuse.plot()
plt.ylabel('Irradiance (W/m**2)')



#POA ground diffuse

poa_ground_diffuse = pvlib.irradiance.grounddiffuse(surface_tilt, tmy_data['GHI'], albedo=albedo)
poa_ground_diffuse.plot()
plt.ylabel('Irradiance (W/m**2)')

#Calculate AOI

aoi = pvlib.irradiance.aoi(surface_tilt, surface_azimuth, solpos['apparent_zenith'], solpos['azimuth'])
aoi.plot()
plt.ylabel('Angle of incidence (deg)')

#POA total

poa_irrad = pvlib.irradiance.total_irrad(surface_tilt, surface_azimuth, solpos['apparent_zenith'], solpos['azimuth'],tmy_data['DNI'], tmy_data['GHI'],tmy_data['DHI'] )
poa_irrad.plot()
plt.ylabel('Irradiance (W/m**2)')
plt.title('POA Irradiance')

#cell and module temperature
pvtemps = pvlib.pvsystem.sapm_celltemp(poa_irrad['poa_global'], tmy_data['Wspd'], tmy_data['DryBulb'])

pvtemps.plot()
plt.ylabel('Temperature (C)')

#DC power using SAPM
sandia_modules = pvlib.pvsystem.retrieve_sam(name='SandiaMod') # This opens up a database called sandia_modules
sandia_module = sandia_modules.Canadian_Solar_CS5P_220M___2009_ # This selects a particular module from the database

#calculate the effective irradiance
effective_irradiance = pvlib.pvsystem.sapm_effective_irradiance(poa_irrad.poa_direct, poa_irrad.poa_diffuse, airmass, aoi, sandia_module)

#Run the SAPM using the parameters calculated above
sapm_out = pvlib.pvsystem.sapm(effective_irradiance, pvtemps.temp_cell, sandia_module)
print(sapm_out.head())
sapm_out[['p_mp']].plot()
plt.ylabel('DC Power (W)')

#AC Power using SAPM
sapm_inverters = pvlib.pvsystem.retrieve_sam('sandiainverter') # Again, this opens up a database
sapm_inverter = sapm_inverters['ABB__MICRO_0_25_I_OUTD_US_208_208V__CEC_2014_']
sapm_inverter

p_acs = pd.DataFrame()
p_acs['sapm'] = pvlib.pvsystem.snlinverter(sapm_out.v_mp, sapm_out.p_mp, sapm_inverter)

p_acs.plot()
plt.ylabel('AC Power (W)')

p_acs.loc['2015-07-05':'2015-07-06'].plot()

