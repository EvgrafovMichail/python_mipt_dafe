import numpy as np



def mse(y_pred, y_test):
    return np.sum((y_pred - y_test) ** 2) / (y_pred.shape[0])



def mae(y_pred, y_test):
    return np.sum(abs(y_pred - y_test)) / (y_pred.shape[0])



def r_score(y_pred, y_test):
    return 1 - (np.sum((y_pred - y_test) ** 2) / np.sum((y_pred - np.mean(y_pred)) ** 2))



def accuracy(y_pred, y_test):
    return np.sum(y_pred == y_test)/(y_pred.shape[0])



def rmse(y_pred, y_test):
    return np.sqrt(mse(y_pred, y_test))


def precision_score(y_pred, y_test):
    TP = np.sum((y_pred == 1) & (y_test == 1))
    FP = np.sum((y_pred == 1) & (y_test == 0))
    return TP / (TP + FP)

def recall_score(y_pred, y_test):
    TP = np.sum((y_pred == 1) & (y_test == 1))
    FN = np.sum((y_pred == 0) & (y_test == 1))
    return TP / (TP + FN)

def f1_score(y_pred, y_test):
    p = precision_score(y_pred, y_test)
    r = recall_score(y_pred, y_test)
    return (2 * (p * r)) / (p + r)

