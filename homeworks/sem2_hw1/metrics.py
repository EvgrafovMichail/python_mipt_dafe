import numpy as np
from enum import Enum


class ShapeMismatchError(Exception):
    pass


def l1(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a.copy()
    b = b.copy()

    if a.ndim == 1:
        a = a.reshape(a.shape[0], 1)
        b = b.reshape(b.shape[0], 1)

    a = a.reshape(a.shape[0], 1, a.shape[1])

    return np.sum(abs(a - b), axis=-1)


def l2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = a.copy()
    b = b.copy()

    if a.ndim == 1:
        a = a.reshape(a.shape[0], 1)
        b = b.reshape(b.shape[0], 1)

    a = a.reshape(a.shape[0], 1, a.shape[1])

    return np.sum((a - b) ** 2, axis=-1)**0.5


def MSE(ordinates: np.ndarray, predict: np.ndarray):
    return np.sum((predict - ordinates) ** 2) / (ordinates.shape[0])


def MAE(ordinates: np.ndarray, predict: np.ndarray):
    return np.sum(abs(predict - ordinates)) / (ordinates.shape[0])


def R_2(ordinates: np.ndarray, predict: np.ndarray):
    return 1 - np.sum((predict - ordinates) ** 2) / np.std(ordinates)


def accuracy(ordinates: np.ndarray, predict: np.ndarray):
    return np.sum(ordinates == predict) / (ordinates.shape[0])


class Metric(Enum):
    l1 = l1
    l2 = l2
    MAE = MAE
    MSE = MSE
    R_2 = R_2
    accuracy = accuracy


if __name__ == "__main__":
    a = np.array([[1, 0], [2, 2]])
    b = np.array([[0, 0], [0, 1]])
    print(l2(a, b))
