import numpy as np



def mse(y_pred, y_test):
    return np.sum((y_pred - y_test) ** 2) / (y_pred.shape[0])



def mae(y_pred, y_test):
    return np.sum(abs(y_pred - y_test)) / (y_pred.shape[0])



def r_score(y_pred, y_test):
    return 1 - (np.sum((y_pred - y_test) ** 2) / np.sum((y_pred - np.mean(y_pred)) ** 2))



def accuracy(y_pred, y_test):
    return np.sum(y_pred == y_test)/(y_pred.shape[0])
