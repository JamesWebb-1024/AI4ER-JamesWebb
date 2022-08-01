from AnomalyRemoval import maskarray
import csv
import netCDF4
import numpy as np
import pandas as pd

# This is all the lakes recorded by the satellites, minus the ones with missing diversity, npp or rhow variables.
lakes = ['Austria_01', 'Austria_02', 'Austria_03', 'Austria_04', 'Austria_05', 'Austria_06', 'Croatia_01',
         'France_01', 'France_02', 'France_03', 'France_04', 'France_05', 'France_06',
         'France_07', 'Germany_04', 'Germany_05', 'Germany_06', 'Germany_07', 'Germany_08',
         'Germany_10', 'Germany_11', 'Italy_01', 'Italy_02', 'Italy_03', 'Italy_04',
         'Italy_07', 'Italy_08', 'Slovenia_01', 'Sweden_01', 'Sweden_02', 'Sweden_03', 'Sweden_04',
         'Sweden_05', 'Sweden_06', 'Sweden_07', 'Sweden_09', 'Sweden_10', 'Sweden_11', 'Sweden_12', 'Sweden_15',
         'Sweden_16', 'Sweden_18', 'Sweden_19', 'Sweden_20', 'Sweden_21', 'Sweden_22', 'Sweden_23', 'Sweden_25',
         'Sweden_35', 'Switzerland_01', 'Switzerland_03', 'Switzerland_04']

# These are the headers for the variables from the .nc files.
DataHeaders13band = {'rtoa_B1': [], 'rtoa_B2': [], 'rtoa_B3': [], 'rtoa_B4': [], 'rtoa_B5': [], 'rtoa_B6': [],
                     'rtoa_B7': [], 'rtoa_B8A': [], 'rtoa_B9': [], 'rhow_B1': [], 'rhow_B2': [], 'rhow_B3': [],
                     'rhow_B4': [], 'rhow_B5': [],
                     'rhow_B6': [], 'rhow_B7': [], 'rhow_B8A': [], 'rhown_B1': [], 'rhown_B2': [], 'rhown_B3': [],
                     'rhown_B4': [], 'rhown_B5': [], 'rhown_B6': [], 'iop_apig': [], 'iop_adet': [], 'iop_agelb': [],
                     'iop_bpart': [], 'iop_bwit': [], 'iop_adg': [], 'iop_atot': [], 'iop_btot': [], 'kd489': [],
                     'kdmin': [], 'kd_z90max': [], 'conc_tsm': [], 'conc_chl': []}


# Function to extract means from a 13 band .nc file
def extract_means_13(filename):
    data = netCDF4.Dataset(filename)
    variables = ['rtoa_B1', 'rtoa_B2', 'rtoa_B3', 'rtoa_B4', 'rtoa_B5', 'rtoa_B6', 'rtoa_B7', 'rtoa_B8A',
                 'rtoa_B9', 'rhow_B1', 'rhow_B2', 'rhow_B3', 'rhow_B4', 'rhow_B5',
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


# Function to extract means from a 21 band .nc file
def extract_means_21(filename):
    data = netCDF4.Dataset(filename)
    variables = ['rtoa_3', 'rtoa_4', 'rtoa_6', 'rtoa_8', 'rtoa_11', 'rtoa_12', 'rtoa_16', 'rtoa_17',
                 'rtoa_20', 'rhow_3', 'rhow_4', 'rhow_6', 'rhow_8', 'rhow_11',
                 'rhow_12', 'rhow_16', 'rhow_17', 'rhown_3', 'rhown_4', 'rhown_6', 'rhown_8', 'rhown_11',
                 'rhown_12', 'iop_apig', 'iop_adet', 'iop_agelb', 'iop_bpart', 'iop_bwit', 'iop_adg', 'iop_atot',
                 'iop_btot', 'kd489', 'kdmin', 'kd_z90max', 'conc_tsm', 'conc_chl']
    means = []
    for i in range(0, len(variables)):
        array = np.array(data[variables[i]])
        marray = maskarray(array)
        avg = np.mean(marray)
        means.append(avg)

    return means


# Import some examples to tell which satellite an image is from.
example_13 = netCDF4.Dataset('All_Lakes/Austria_02.nc')
example_21 = netCDF4.Dataset('All_Lakes/Austria_01.nc')

# Initialise an empty dataframe
meandf = pd.DataFrame(
    columns=DataHeaders13band,
    index=lakes
)

# Loop over all the lakes, identify which satellite they are from and then add them into the dataframe
for lake in lakes:
    data = netCDF4.Dataset('All_Lakes/' + lake + '.nc')
    if data.variables.keys() == example_13.variables.keys():
        print(lake+': 13band')
        means = extract_means_13('All_Lakes/' + lake + '.nc')
        meandf.loc[lake, :] = means
    elif data.variables.keys() == example_21.variables.keys():
        print(lake + ': 21band')
        means = extract_means_21('All_Lakes/' + lake + '.nc')
        meandf.loc[lake, :] = means
    else:
        print(lake + " matches neither satellite, don't include in future.")

# import the .csv containing the catchment area data
Catch_Data = pd.read_csv('Catchment_Funct_Div.csv')

# Create an empty df to put all the .csv data into
Relevant_Data = pd.DataFrame(
    columns=Catch_Data.columns,
    index=lakes
)

# Loop over all the lakes adding the lake needed into the dataframe.
for lake in lakes:
    row = Catch_Data[Catch_Data['Lake'] == lake]
    print(lake)
    Relevant_Data.loc[lake, :] = list(np.array(row))[0]

# Remove unneeded columns from csv
ColumnsToRemove = ['LAKE.ID', 'Date', 'NDVI', 'SSM', 'Nitro', 'OCD', 'ocs', 'sand', 'silt', 'soc',
                   'catchment_area', 'lake_area', 'lake_peri', 'mean_pop_density', 'n_lakes', 'Lake_area', 'Shore_len',
                   'Shore_dev', 'Vol_total', 'Vol_res', 'Vol_src', 'Depth_avg', 'Dis_avg', 'Res_time', 'Elevation',
                   'Slope_100', 'Wshd_area', 'Pour_long', 'Pour_lat',
                   'DOC', 'DN', 'Funct_Diversity', 'Latitude', 'Longitude', 'si10.1', 't2m.1', 'cdir.1', 'uvb.1',
                   'e.1', 'cvh.1', 'lmld.1', 'lmlt.1', 'lai_hv.1', 'lai_lv.1', 'cvl.1', 'mror.1', 'ro.1', 'sro.1',
                   'tp.1', 'tvh.1',
                   'tvl.1', 'BPP', 'Water_Temp', 'pH', 'Secchi', 'BBE_cDOM', 'abs400', 'abs254', 'Resp', 'BPP_Carbon',
                   'Chla']
for col in ColumnsToRemove:
    del Relevant_Data[col]

# Separate Diversity Column into its own file
YData = Relevant_Data['Diversity']
del Relevant_Data['Diversity']


DataCombined = pd.concat([meandf, Relevant_Data], axis=1)
print(DataCombined)

FileSaveName = 'AllLakes'
# Save them to a .csv file named based on tg=he given variable at the top.
DataCombined.to_csv(FileSaveName + 'XData.csv', index=False)
YData.to_csv(FileSaveName + 'YData.csv', index=False)






