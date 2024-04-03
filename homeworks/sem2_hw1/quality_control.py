import numpy as np


def mean_squared_error(
        original: np.ndarray,
        predicted: np.ndarray,
):
    mse = np.sum((original - predicted) ** 2) / len(original)

    return mse


def mean_absolute_error(
        original: np.ndarray,
        predicted: np.ndarray,
):
    mae = np.sum(np.abs(original - predicted)) / len(original)

    return mae


def rss(
        original: np.ndarray,
        predicted: np.ndarray,
):
    numerator = np.sum((original - predicted) ** 2)
    denominator = np.sum((original - np.mean(predicted)) ** 2)
    rss = 1 - numerator / denominator

    return rss


def accuracy(
        original: np.ndarray,
        predicted: np.ndarray,
):
    return np.sum(original == predicted) / len(original)
