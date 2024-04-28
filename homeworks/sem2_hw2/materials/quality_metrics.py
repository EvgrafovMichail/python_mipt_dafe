import numpy as np


def MeanSquaredError(y_predicted: np.ndarray, y_expected: np.ndarray):
    MSE = np.sum((y_expected - y_predicted) ** 2) / y_predicted.shape[0]
    return MSE


def MeanAbsoluteError(y_predicted: np.ndarray, y_expected: np.ndarray):
    MAE = np.sum(np.abs(y_expected - y_predicted)) / y_predicted.shape[0]
    return MAE


def determination_coef(y_predicted: np.ndarray, y_expected: np.ndarray):
    R2 = 1 - np.sum((y_expected - y_predicted)**2) / np.sum((y_expected - np.mean(y_expected))**2)
    return R2


def get_accuracy_score(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    accuracy = np.sum(prediction == expectation) / expectation.shape[0]
    return accuracy
