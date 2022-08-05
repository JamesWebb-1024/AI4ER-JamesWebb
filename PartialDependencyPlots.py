from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.inspection import PartialDependenceDisplay
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

X = pd.read_csv('NewDatasets/TrimmedXData.csv')
y = pd.read_csv('NewDatasets/TrimmedYData.csv')

fig = plt.figure()
pd.plotting.scatter_matrix(X, figsize = (40,40), alpha = 0.9, diagonal="kde",marker="o")
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)
fig.show()


'''
from sklearn.datasets import load_iris
X, y = make_hastie_10_2(random_state=0)
clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,
    max_depth=1, random_state=0).fit(X, y)
features = [0, 1, (0, 1)]
PartialDependenceDisplay._plot_one_way_partial_dependence(clf, X, features)
'''