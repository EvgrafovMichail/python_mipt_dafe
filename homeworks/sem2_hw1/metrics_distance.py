import numpy as np


class ShapeMismatchError(Exception):
    pass


def distance(t_abscissa: np.ndarray, abscissa: np.ndarray, metric: str) -> np.ndarray:
    if metric == 'l1':
        # Calculate Manhattan distance (L1 norm) between each pair of points
        dist = np.linalg.norm(t_abscissa - abscissa[:, np.newaxis], axis=-1, ord=1)

    elif metric == 'l2':
        # Calculate Euclidean distance (L2 norm) between each pair of points
        dist = np.linalg.norm(t_abscissa - abscissa[:, np.newaxis], axis=-1)
    return dist


def MSE(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """
    Вычисляет среднеквадратичную ошибку (MSE) между предсказанными и истинными значениями.
    """
    s = np.mean((y_true - y_pred) ** 2)
    return s


def MAE(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """
    Вычисляет среднюю абсолютную ошибку (MAE) между предсказанными и истинными значениями.
    """
    s = np.mean(np.abs(y_true - y_pred))
    return s


def rr(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """
    Вычисляет коэффициент детерминации (R-квадрат) между предсказанными и истинными значениями.
    """
    return 1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)


def accuracy(y_pred: np.ndarray, y_true: np.ndarray) -> float:
    """Вычисляет точность для задач классификации."""
    return np.mean(y_true == y_pred)
