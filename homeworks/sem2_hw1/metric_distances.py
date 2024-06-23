import numpy as np


def distance(t_abscissa: np.ndarray, abscissa: np.ndarray, metric: str) -> np.ndarray:
    if metric == 'l1':
        dist = np.linalg.norm(t_abscissa - abscissa[:, np.newaxis], axis=-1, ord=1)
    elif metric == 'l2':
        dist = np.linalg.norm(t_abscissa - abscissa[:, np.newaxis], axis=-1)
    else:
        raise ValueError("Invalid metric. Must be either 'l1' or 'l2'.")
    return dist


def MSE(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    return np.mean((y_true - y_pred) ** 2)


def MAE(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    return np.mean(np.abs(y_true - y_pred))


def rr(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    return 1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)


def accuracy(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    return np.mean(y_true == y_pred)
