import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pickle

# Import the data
Data = pd.read_csv('ChemDivFinalData.csv')

# Extract X and y from the data

y = Data['Diversity']

X = Data
del(X['Diversity'])

# Initialise the forest and train it
forest = RandomForestRegressor(n_jobs=-1, max_depth=7, n_estimators=10000)
forest.fit(Data, np.ravel(y))

# Save the model to a .pkl (Pickle) file
pkl_filename = 'ChemDivFinalModel.pkl'
with open(pkl_filename, 'wb') as file:
    pickle.dump(forest, file)

# Open the file to calculate scores or use it to predict results
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)