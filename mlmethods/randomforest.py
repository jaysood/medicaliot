#####################################################
#   KNN classifier implementation                   #
#                                                   #
#   Author: Jay Rauniar Sood - 2019/2020            #
#####################################################


import convert, ml_metrics, matplotlib
matplotlib.use('macosx')
import numpy as np
import pandas as pd
from sklearn import ensemble, model_selection
from datetime import datetime

cf_labels = ["MT", "SI", "MW", "ST", "RPM", "AP", "SC", "MMC"]

#Dump data to CSV for input to algorithm
nametable = convert.convert(return_nametable = True)
ml_dataframe = pd.read_csv('ml_data.csv', names = ["CPU", " Width", "Length", "Height",
                                                   "Weight", "Sensor 1", "Sensor 2", "Sensor 3",
                                                   "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7",
                                                   "Connect 1", "Connect 2", "Connect 3", "Class"])

#DATA PREPROCESSING
ml_dataframe.replace(0, -1, inplace = True)
FEATURES = np.array(ml_dataframe.drop(['Class'], 1))
CLASS = np.array(ml_dataframe['Class'])

#Cross validation, splitting data into test and training set.
FEATURES_TRAIN, FEATURES_TEST, CLASS_TRAIN, CLASS_TEST = model_selection.train_test_split(FEATURES, CLASS, test_size = 0.33)

#Train RF classifier on training set + time metric
start_time = datetime.now()
rf_classifier =  ensemble.RandomForestClassifier(n_estimators = 10)
rf_classifier.fit(FEATURES_TRAIN, CLASS_TRAIN)
training_time = datetime.now() - start_time

#OUTPUT METRICS
metric_table = ml_metrics.outputMetrics(rf_classifier, FEATURES_TRAIN, CLASS_TRAIN, FEATURES_TEST,
                                        CLASS_TEST, training_time, cf_labels, average_type = "macro")

pd.options.display.float_format = '{:20,.6f}'.format

print(metric_table)
