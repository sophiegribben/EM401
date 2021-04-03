# Domestic Load Profile Synthesis for LV network simulation at scale
A repository to store code from my dissertation project, carried out under the supervision of Dr Bruce Stephen from September 2020 - March 2021. 

## Files


### lcl_shape_syth
Using low carbon london and guassian methods to synthesise load profiles. Requires the lcl_clean_widefmt.csv file. 
 * guassian_model contains 3 functions to generate a day, week or year worth of profiles
 * master.py can be used to generate a year of profiles (output to csv file)
 * plotting_script generates graphs for my final report

#### elexon-class-1
Script and files to work with elexon profile class 1. 
 * extract_profile1 
	- splits up the ELEXON profile class 1 for plotting purposes
	- builds 1 year of elexon profile class 1 (outputs csv file)
 * ProfileClass1.csv 

### REFIT (unfinished)
Using the REFIT household load profiles to build profiles based on appliance start times.
 * REFIT_profile extracts the start times of appliances

### open-dss-v2
Network model developed by Dr Rory Telford
 * error-analysis folder contains files and scripts used to compare lcl_shape_syth model to CREST, ELEXON and Low Carbon London data

### python learning
 * for misc. scripts used to familiarise myself with python

## Other Documents
All documents related to the project are stored on my University OneDrive. 
