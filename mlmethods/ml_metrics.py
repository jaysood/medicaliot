import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

def generateConfusionMatrix(classifier, y_test, predicted, title = None, labels = None, plot = False):
    conf_matrix = metrics.confusion_matrix(y_test, predicted)
    conf_disp = metrics.ConfusionMatrixDisplay(conf_matrix, labels)
    if plot:
        conf_disp.plot(cmap=plt.cm.Blues)
        plt.show()
    return conf_matrix


def outputMetrics(classifier, x_train, y_train, x_test, y_test, time, matrix_labels, average_type, normalize = True):
    metric_data = {}
    predicted = np.array(classifier.predict(x_test))

    # Generating confusion matrix
    conf_matrix = generateConfusionMatrix(classifier, y_test, predicted, labels = matrix_labels, plot = True)

    metric_data["Accuracy"] = accuracy(y_test, predicted, normalize)
    metric_data["True Positive Rate"] = trueFalsePosNegRate(conf_matrix, statistic = "TPR")
    metric_data["False Positive Rate"] = trueFalsePosNegRate(conf_matrix, statistic = "FPR")
    metric_data["Precision"] = precision(y_test, predicted, average_type)
    metric_data["Recall"] = recall(y_test, predicted, average_type)
    metric_data["F-Measure"] = fMeasure(y_test, predicted, average_type)
    # metric_data["Area under ROC"] = areaUnderRoc(y_test, predicted, plot = True)
    metric_data["Training Time"] = int(time.microseconds)

    converted_metric_data = pd.DataFrame.from_dict(metric_data.items())

    return converted_metric_data


def accuracy(expected, predicted, normalize):
    output = metrics.accuracy_score(expected, predicted, normalize)
    return output

def trueFalsePosNegRate(matrix, statistic):
    total_true_positive = np.sum(np.diag(matrix))
    total_false_positive = sum(matrix.sum(axis = 0) - np.diag(matrix))
    total_false_negative = sum(matrix.sum(axis = 1) - np.diag(matrix))
    total_true_negative = matrix.sum() - (total_true_positive + total_false_positive + total_false_negative)

    if statistic == "TPR":
        TPR = total_true_positive/(total_true_positive + total_false_negative)
        return TPR
    elif statistic == "FPR":
        FPR = total_false_positive/(total_false_positive + total_true_negative)
        return FPR
    elif statistic == "FNR":
        FNR = total_false_negative/(total_true_positive + total_false_negative)
        return FNR
    elif statitic == "TNR":
        TNR = total_true_negative/(total_true_negative + total_false_positive)
        return TNR

def precision(expected, predicted, average_type):
    output = metrics.precision_score(expected, predicted, average = average_type)
    return output

def recall(expected, predicted, average_type):
    output = metrics.recall_score(expected, predicted, average = average_type)
    return output

def fMeasure(expected, predicted, average_type):
    output = metrics.f1_score(expected, predicted, average = average_type)
    return output

def areaUnderRoc(y_test, predicted, plot = False):
    roc_false_positive, roc_true_positive, threshold = metrics.roc_curve(y_test, predicted)
    area_under_roc = metrics.auc(roc_false_positive, roc_true_positive)
    if plot == True:
        plt.figure(figsize = (8,8), dpi = 150)
        plt.plot(roc_false_positive, roc_true_positive, linestyle = '-')
        plt.xlabel('FPR')
        plt.ylabel('TPR')
        plt.legend()
        plt.show()
    return area_under_roc
