import numpy as np
from typing import Iterable

from data_controler.exceptions import ShapeMismatchError


class Metric():
    __metrics: list = ["accuracy", "determination_coef", "MAE", "MSE"]
    __distances: list = ["MAE", "MSE"]

    @staticmethod
    def cheak_metric(metric: str) -> bool:
        if metric in Metric.__metrics:
            return True
        else:
            return False

    @staticmethod
    def cheak_distances(distances: str) -> bool:
        if distances in Metric.__distances:
            return True
        else:
            return False

    @staticmethod
    def get_score(targets: Iterable, predicts: Iterable, metric: str) -> float:
        _targets = np.array(targets).flatten()
        _predicts = np.array(predicts).flatten()

        if _targets.size != _predicts.size:
            raise ShapeMismatchError(
                f'targets size: {_targets.size} / predicts size: {_predicts.size}'
            )

        if metric == "accuracy":
            return np.sum(_targets == _predicts) / _targets.size
        elif metric == "determination_coef":
            return 1 - np.sum(np.power(_predicts - _targets, 2)) / np.sum(
                   np.power(np.mean(_targets) - _targets, 2)
            )
        elif metric == "MAE":
            return np.sum(_predicts - _targets) / _targets.size
        elif metric == "MSE":
            return np.sum(np.power(_predicts - _targets, 2)) / _targets.size
        else:
            raise ValueError(
                f"The {metric} metric is not provided for get_score"
            )

    @staticmethod
    def get_distance(x1: np.ndarray, x2: np.ndarray, distance: str) -> float:
        if distance == "MAE":
            return np.sum(np.abs(x1 - x2))
        elif distance == "MSE":
            return np.sum(np.power(x1 - x2, 2))
        else:
            raise ValueError(
                f"The {distance} distance is not provided for get_distance"
            )
