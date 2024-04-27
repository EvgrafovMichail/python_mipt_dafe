import numpy as np


def mean_squared_error(
        original: np.ndarray,
        predicted: np.ndarray,
) -> float:
    mse = np.round(np.sum((original - predicted) ** 2) / len(original), 2)

    return mse


def mean_absolute_error(
        original: np.ndarray,
        predicted: np.ndarray,
) -> float:
    mae = np.round(np.sum(np.abs(original - predicted)) / len(original), 2)

    return mae


def determination_coef(
        original: np.ndarray,
        predicted: np.ndarray,
) -> float:
    numerator = np.sum((original - predicted) ** 2)
    denominator = np.sum((original - np.mean(predicted)) ** 2)
    determination_coef = np.round(1 - numerator / denominator, 2)

    return determination_coef


def accuracy(
        original: np.ndarray,
        predicted: np.ndarray,
) -> float:
    accur = np.round(np.sum(original == predicted) / len(original), 4)
    return accur
