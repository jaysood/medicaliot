import numpy as np
import convert
import pandas as pd
import seaborn as sn
import matplotlib
matplotlib.use('macosx')
import matplotlib.pyplot as plt
from sklearn import preprocessing, neighbors, metrics, model_selection

cf_labels = []


#Dump data to CSV for input to algorithm
nametable = convert.convert(return_nametable = True)
ml_dataframe = pd.read_csv('ml_data.csv', names = ["CPU", "Width", "Length", "Height",
                                                   "Weight", "Sensor 1", "Sensor 2", "Sensor 3",
                                                   "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7",
                                                   "Connect 1", "Connect 2", "Connect 3", "Class"])

#DATA PREPROCESSING
ml_dataframe.replace(0, -1, inplace = True)
FEATURES = np.array(ml_dataframe.drop(['Class'], 1))
CLASS = np.array(ml_dataframe['Class'])


#Cross validation, splitting data into test and training set.
FEATURES_TRAIN, FEATURES_TEST, CLASS_TRAIN, CLASS_TEST = model_selection.train_test_split(FEATURES, CLASS, test_size = 0.5)

#Train KNN classifier on training set
knn_classifier =  neighbors.KNeighborsClassifier(n_neighbors = 9)
knn_classifier.fit(FEATURES_TRAIN, CLASS_TRAIN)

#Make class predictions for testing set
CLASS_PREDICT = knn_classifier.predict(FEATURES_TEST)
print(metrics.accuracy_score(CLASS_TEST, CLASS_PREDICT))


#Generating confusion matrix
np.set_printoptions(suppress = True)

for item in nametable.values():
    cf_labels.append(item)

disp_matrix = metrics.plot_confusion_matrix(knn_classifier, FEATURES_TEST, CLASS_TEST, display_labels = cf_labels, cmap=plt.cm.Blues)
disp_matrix.ax_.set_title("KNN Confusion Matrix for IoMT Data")
print(disp_matrix.confusion_matrix)
plt.show()
