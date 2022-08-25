import numpy as np
import pandas as pd

# Import the csv containing all the data
Catch_Data = pd.read_csv('(V2)Catchment_Func_Div.csv')

# Specify which lakes are to be included in the training set (This is all but 5 outliers)
lakelist = ['Austria_01', 'Austria_02', 'Austria_03', 'Austria_07', 'Croatia_01', 'Croatia_02', 'Croatia_03',
            'Croatia_04', 'Denmark_01', 'Finland_02', 'Finland_03', 'Finland_04', 'Finland_05', 'Finland_06',
            'Finland_07', 'Finland_08', 'Finland_09', 'Finland_13', 'Finland_16', 'Finland_17', 'France_02',
            'France_04', 'France_05', 'France_06', 'France_07', 'Germany_02', 'Germany_03', 'Germany_04',
            'Germany_05', 'Germany_07', 'Germany_09', 'Germany_10', 'Germany_11', 'Italy_01', 'Italy_02', 'Italy_03',
            'Italy_05', 'Italy_06', 'Italy_07', 'Italy_08', 'Norway_01', 'Norway_02', 'Norway_04', 'Norway_05',
            'Norway_07', 'Norway_08', 'Norway_10', 'Norway_12', 'Norway_13', 'Norway_14', 'Poland_01', 'Poland_02',
            'Slovenia_01', 'Sweden_02', 'Sweden_03', 'Sweden_04', 'Sweden_05', 'Sweden_06', 'Sweden_07', 'Sweden_08',
            'Sweden_09', 'Sweden_10', 'Sweden_11', 'Sweden_14', 'Sweden_15', 'Sweden_16', 'Sweden_17', 'Sweden_18',
            'Sweden_182', 'Sweden_19', 'Sweden_20', 'Sweden_22', 'Sweden_24', 'Sweden_25', 'Sweden_26', 'Sweden_28',
            'Sweden_29', 'Sweden_32', 'Sweden_33', 'Sweden_34', 'Sweden_35', 'Sweden_38', 'Sweden_39', 'Sweden_40',
            'Sweden_41', 'Sweden_43', 'Sweden_44', 'Sweden_45', 'Sweden_46', 'Sweden_48']

# Specify the columns from the catchment csv to keep, in the order that they will be put into the new dataset.
varlist = ['Lake', 'NPP', 'Pastures', 'Peat.bogs', 'Non.irrigated.arable.land', 'Complex.cultivation.patterns',
           'Land.principally.occupied.by.agriculture.with.significant.areas.of.natural.vegetation',
           'Natural.grasslands', 'Beaches.dunes.sands', 'Discontinuous.urban.fabric', 'Green.urban.areas',
           'Invsimpson']

# Specify the filename that the data will be saved as
filename = 'FinalData'

# Create an empty df to put all the .csv data into
Relevant_Rows = pd.DataFrame(
    columns=Catch_Data.columns,
    index=lakelist
)

# Extract the necessary rows from the csv and put them into Relevant_Rows.
for lake in lakelist:
    print(lake)
    row = Catch_Data[Catch_Data['Lake'] == lake]
    # If there is an error on this line, it is most likely because one of the lakes in lakelist is not in Catch_Data.
    Relevant_Rows.loc[lake, :] = list(np.array(row))[0]


# Extract the relevant columns from Relevant_Rows and put them into Relevant_Cols
Relevant_Cols = Relevant_Rows[varlist[0]]
for i in range(1, len(varlist)):
    col = Relevant_Rows[varlist[i]]
    Relevant_Cols = pd.concat([Relevant_Cols, col], axis=1)

# Export the final array to a csv with name filename.
Relevant_Cols.to_csv(filename+'.csv', index = False)