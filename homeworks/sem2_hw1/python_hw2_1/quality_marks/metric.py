import numpy as np


def MSE(prediction: np.ndarray,
        expectation: np.ndarray
        ):
    return np.sum((prediction-expectation)**2)/(prediction.shape[0])


def MAE(prediction: np.ndarray,
        expectation: np.ndarray
        ):
    return np.sum(np.abs(prediction-expectation))/(prediction.shape[0])


def R_2(prediction: np.ndarray,
        expectation: np.ndarray
        ):
    return 1 - np.sum((prediction-expectation)**2)/np.sum((prediction - np.mean(expectation))**2)


def get_accuracy_score(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    return np.sum(prediction == expectation)/(prediction.shape[0])
