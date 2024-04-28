import numpy as np
from ultralib999.dev_only.Helpers import _could_be_compared


def mse(y_true: np.ndarray, y_pred: np.ndarray, ) -> float:
    _could_be_compared(y_true, y_pred)
    return ((y_true - y_pred) ** 2).sum() / y_pred.size


def mae(y_true: np.ndarray, y_pred: np.ndarray, ) -> float:
    _could_be_compared(y_true, y_pred)

    return (np.abs(y_true - y_pred)).sum() / y_pred.shape[0]


# тут непонятно было написано что должно быть в знаменателе, я определил так
def r_pow_2(y_true: np.ndarray, y_pred: np.ndarray, ) -> float:
    _could_be_compared(y_true, y_pred)
    return 1 - ((y_true - y_pred) ** 2).sum() / ((y_true - y_true.mean()) ** 2).sum()


def accuracy(y_true: np.ndarray, y_pred: np.ndarray, ) -> float:
    _could_be_compared(y_true, y_pred)
    return np.in1d(y_true, y_pred).astype(int).sum() / y_pred.size
