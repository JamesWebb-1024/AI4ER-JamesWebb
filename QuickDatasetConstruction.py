import pandas as pd
import numpy as np

FileSaveName = 'Austria'

lakelist = ['Austria_01', 'Austria_02', 'Austria_03', 'Austria_04', 'Austria_05', 'Austria_06']

AllXData = pd.read_csv('AllLakesXData.csv')
AllYData = pd.read_csv('AllLakesYData.csv')

AllData = pd.concat([AllXData, AllYData], axis=1)

# Create an empty df to put all the .csv data into
Relevant_Data = pd.DataFrame(
    columns=AllData.columns,
    index=lakelist
)

# Extract the necessary rows from the csv and put them into Relevant_Data.
for lake in lakelist:
    row = AllData[AllData['Lake'] == lake]
    Relevant_Data.loc[lake, :] = list(np.array(row))[0]


del Relevant_Data['Lake']

YData = Relevant_Data['Diversity']
del Relevant_Data['Diversity']
XData = Relevant_Data


XData.to_csv('NewDatasets/' + FileSaveName + 'XData.csv', index=False)
YData.to_csv('NewDatasets/' + FileSaveName + 'YData.csv', index=False)