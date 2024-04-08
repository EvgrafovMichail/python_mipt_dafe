import numpy as np


def MSE(ordinates: np.ndarray, predict: np.ndarray):
    return np.sum((predict - ordinates) ** 2) / (ordinates.shape[0])


def MAE(ordinates: np.ndarray, predict: np.ndarray):
    return np.sum(abs(predict - ordinates)) / (ordinates.shape[0])


def R_2(ordinates: np.ndarray, predict: np.ndarray):
    return 1 - np.sum((predict - ordinates) ** 2) / np.std(ordinates)


def accuracy(ordinates: np.ndarray, predict: np.ndarray):
    return np.sum(ordinates == predict) / (ordinates.shape[0])
