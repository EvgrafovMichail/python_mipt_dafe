import numpy as np


def MSE(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    return np.sum((prediction-expectation)**2)/(prediction.shape[0])


def MAE(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    return np.sum(np.abs(prediction-expectation))/(prediction.shape[0])


def get_determination(
    prediction: np.ndarray,
    expectation: np.ndarray,
) -> float:
    rss = np.sum((expectation - prediction) ** 2)
    result = 1 - (rss / np.sum((expectation - np.mean(expectation)) ** 2))

    return result


def get_accuracy_score(
    prediction: np.ndarray,
    expectation: np.ndarray
) -> float:
    matching = prediction == expectation
    accuracy = np.sum(matching) / expectation.size

    return accuracy
