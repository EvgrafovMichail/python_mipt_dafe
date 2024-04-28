import numpy as np


def MSE(
    received: np.ndarray,
    original: np.ndarray
) -> float:
    if not (original.shape[0] == received.shape[0]):
        raise ValueError("different dim")
    return np.sum((received - original) ** 2) / received.shape[0]


def MAE(
    received: np.ndarray,
    original: np.ndarray
) -> float:
    if not (original.shape[0] == received.shape[0]):
        raise ValueError("different dim")
    return np.sum(np.absolute(received - original)) / received.shape[0]


def R_in_square(
    received: np.ndarray,
    original: np.ndarray
) -> float:
    if not (original.shape[0] == received.shape[0]):
        raise ValueError("different dim")

    mse_multilpy_n = received.shape[0] * MSE(received, original)
    mean_error = np.sum((original - np.mean(original)) ** 2)
    return 1 - (mse_multilpy_n / mean_error)


def accuracy(
    received: np.ndarray,
    original: np.ndarray
) -> float:
    if not (original.shape[0] == received.shape[0]):
        raise ValueError("different dim")
    return np.sum(original == received) / original.shape[0]
