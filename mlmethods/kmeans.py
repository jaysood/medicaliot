import convert, ml_metrics, matplotlib
matplotlib.use('macosx')
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from datetime import datetime
import matplotlib.pyplot as plt

nametable = convert.convert(return_nametable = True)
ml_dataframe = pd.read_csv('ml_data.csv', names = ["CPU", " Width", "Length", "Height",
                                                   "Weight", "Sensor 1", "Sensor 2", "Sensor 3",
                                                   "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7",
                                                   "Connect 1", "Connect 2", "Connect 3", "Class"])

#DATA PREPROCESSING
# ml_dataframe.replace(0, -1, inplace = True)
FEATURES = np.array(ml_dataframe.drop(['Class'], 1))
CLASS = np.array(ml_dataframe['Class'])

KMeansClassifier = KMeans(n_clusters = 8)
KMeansClassifier.fit(FEATURES)

correct = 0
featurelist = []
featurelist.append(FEATURES)

for i in range(0, len(FEATURES)):
    predict_me = np.array(featurelist[i])
    # predict_me - predict_me.reshape(-1, len(predict_me))
    prediction = KMeansClassifier.predict(predict_me)
    if prediction[0] == CLASS[i]:
        correct += 1

print(correct/len(FEATURES))
