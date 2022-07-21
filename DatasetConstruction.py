from AnomalyRemoval import maskarray
import csv
from AnomalyRemoval import removeoutliers
import netCDF4
import numpy as np
import pandas as pd

# This file will be for constructing the dataset together from the netCDF4 files and the .csv file
# Catchment_Func_Div.

# We need to find the mean of each variable in the netCDF files.

# Function to:
# - Take in a netCDF filename
# - Extract each variable as an array, mask off the 0s and find the mean
# - Return a string of the mean of each band

# There are 40 variables in the netCDF files, and an additional 44 in the .csv file.

MeanDataHeaders = {'rtoa_B1': [], 'rtoa_B2': [], 'rtoa_B3': [], 'rtoa_B4': [], 'rtoa_B5': [], 'rtoa_B6': [],
                   'rtoa_B7': [], 'rtoa_B8': [], 'rtoa_B8A': [], 'rtoa_B9': [], 'rtoa_B10': [], 'rtoa_B11': [],
                   'rtoa_B12': [], 'rhow_B1': [],'rhow_B2': [], 'rhow_B3': [], 'rhow_B4': [], 'rhow_B5': [],
                   'rhow_B6': [], 'rhow_B7': [], 'rhow_B8A': [], 'rhown_B1': [], 'rhown_B2': [], 'rhown_B3': [],
                   'rhown_B4': [], 'rhown_B5': [], 'rhown_B6': [], 'iop_apig': [], 'iop_adet': [], 'iop_agelb': [],
                   'iop_bpart': [], 'iop_bwit': [], 'iop_adg': [], 'iop_atot': [], 'iop_btot': [], 'kd489': [],
                   'kdmin': [], 'kd_z90max': [], 'conc_tsm': [], 'conc_chl': []}
meandf = pd.DataFrame(MeanDataHeaders)


def extract_means(filename):
    data = netCDF4.Dataset(filename)
    variables = ['rtoa_B1', 'rtoa_B2', 'rtoa_B3', 'rtoa_B4', 'rtoa_B5', 'rtoa_B6', 'rtoa_B7', 'rtoa_B8', 'rtoa_B8A',
                 'rtoa_B9', 'rtoa_B10', 'rtoa_B11', 'rtoa_B12', 'rhow_B1', 'rhow_B2', 'rhow_B3', 'rhow_B4', 'rhow_B5',
                 'rhow_B6', 'rhow_B7', 'rhow_B8A', 'rhown_B1', 'rhown_B2', 'rhown_B3', 'rhown_B4', 'rhown_B5',
                 'rhown_B6', 'iop_apig', 'iop_adet', 'iop_agelb', 'iop_bpart', 'iop_bwit', 'iop_adg', 'iop_atot',
                 'iop_btot', 'kd489', 'kdmin', 'kd_z90max', 'conc_tsm', 'conc_chl']
    means = []
    for i in range(0, len(variables)):
        array = np.array(data[variables[i]])
        marray = maskarray(array)
        avg = np.mean(marray)
        means.append(avg)

    return means


lakelist = ['Austria_02', 'Austria_05', 'Croatia_01', 'Croatia_03', 'Germany_04',
            'Germany_05', 'Germany_06', 'Germany_07', 'Germany_08', 'Germany_09', 'Germany_10', 'Germany_11']

for lake in lakelist:
    means = extract_means('20_Lake_Images-Outliers_Included/' + lake + '.nc')
    meandf.loc[len(meandf.index)] = means
# print(meandf)
# data = csv.reader(open('20_Relevant_Catchment_Data.csv'), delimiter=',')

# Read in the csv file as a pandas dataframe and delete Lake, LAKE.ID and Date
# Note that the .csv file being read in here has already had all but the relevant lakes removed, as well as the other
# columns not related to diversity or catchment area.
Catch_Data = pd.read_csv('20_Relevant_Catchment_Data.csv')
del Catch_Data['Lake']
del Catch_Data['LAKE.ID']
del Catch_Data['Date']

DataCombined = pd.concat([meandf, Catch_Data], axis=1)
YData = DataCombined['Diversity']
del DataCombined['Diversity']

print(DataCombined)
print(YData)

DataCombined.to_csv('12LakeXData.csv')
YData.to_csv('12LakeYData.csv')
