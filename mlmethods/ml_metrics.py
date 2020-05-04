import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

def generateConfusionMatrix(classifier, x_data, y_data, title, labels, show):
    c_matrix = metrics.plot_confusion_matrix(classifier, x_data, y_data, display_labels = labels, cmap=plt.cm.Blues)
    c_matrix.ax_.set_title(title)
    if show == True:
        plt.show()
    return c_matrix


def outputMetrics(classifier, x_train, y_train, x_test, y_test, time, average_type, normalize = True):
    metric_data = {}
    predicted = classifier.predict(x_test)

    metric_data["Accuracy"] = accuracy(y_test, predicted, normalize)
    # metric_data["True Positive Rate"] = truePositiveRate()
    # metric_data["False Positive Rate"] = falsePositiveRate()
    metric_data["Precision"] = precision(y_test, predicted, average_type)
    metric_data["Recall"] = recall(y_test, predicted, average_type)
    metric_data["F-Measure"] = fMeasure(y_test, predicted, average_type)
    # metric_data["Area under ROC"] = areaUnderRoc()
    metric_data["Training Time"] = time.microseconds

    converted_metric_data = pd.DataFrame.from_dict(metric_data.items())

    return converted_metric_data


def accuracy(expected, predicted, normalize):
    output = metrics.accuracy_score(expected, predicted, normalize)
    return output

# def truePositiveRate():
#
# def falsePositiveRate():
#
def precision(expected, predicted, average_type):
    output = metrics.precision_score(expected, predicted, average = average_type)
    return output

def recall(expected, predicted, average_type):
    output = metrics.recall_score(expected, predicted, average = average_type)
    return output

def fMeasure(expected, predicted, average_type):
    output = metrics.f1_score(expected, predicted, average = average_type)
    return output

# def areaUnderRoc():
