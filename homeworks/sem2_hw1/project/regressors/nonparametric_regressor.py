import numpy as np
from typing import Union
from ast import Slice
from numbers import Real

from regressors.regressor_abc import RegressorABC
from metrics.metric import Metric


K_NEIGHBOURS = 100


class NonparametricRegressor(RegressorABC):
    _features: np.ndarray[float] = None
    _targets: np.ndarray[float] = None
    _k_neighbours: int = K_NEIGHBOURS
    _distance: str = "MSE"

    def __init__(self, k_neighbours: int = K_NEIGHBOURS, distance: str = "MSE") -> None:
        k_neighbours = int(k_neighbours)

        if k_neighbours <= 0:
            raise ValueError(
                f'invalid k_neighbours value: {k_neighbours}'
                'k_neighbours could have only positive values;'
            )
        if not Metric.cheak_distances(distance):
            raise ValueError(
                f'The {distance} distance is not provided'
            )

        self._distance = distance
        self._k_neighbours = k_neighbours

    def fit(self, features: Slice, targets: Slice) -> None:
        if not isinstance(features, np.ndarray):
            _features = np.ndarray(features, type=float)
        else:
            _features = features
        if not isinstance(targets, np.ndarray):
            _targets = np.array(targets, type=float)
        else:
            _targets = targets
        if _features.shape[0] != _targets.shape[0]:
            raise ValueError(
                'amout of feautures and targets is different'
                f'feautures: {_features.shape[0]} targets: {_targets.shape[0]}'
            )

        self._features = _features
        self._targets = _targets

    def predict(self, features: Union[Real, Slice]
                ) -> Union[float, np.ndarray]:
        if np.any([self._features is None, self._targets is None]):
            raise RuntimeError(
                'method fit() should be called before predict():'
            )
        if self._targets.size <= self._k_neighbours:
            raise ValueError(
                'amount of targets should be more than k_neighbours'
            )
        if isinstance(features, Real):
            return self._compute_predict(np.array(features))[0]
        elif not isinstance(features, np.ndarray):
            features = np.ndarray(features)

        return self._compute_predict(features)

    def _get_weights(self, features: np.ndarray) -> np.ndarray[float]:
        distances = Metric.get_distances(features, self._features, self._distance)
        window = np.sort(distances, axis=1)[:, self._k_neighbours - 1]
        distances = np.divide(distances, window[..., np.newaxis])

        weights = np.subtract(1, np.power(distances, 2))
        weights[weights < 0] = 0
        weights = np.multiply(0.75, weights)

        return weights

    def _compute_predict(self, features: np.ndarray) -> np.ndarray[float]:
        return (
            np.sum(np.multiply(self._targets, self._get_weights(features)), axis=1)
            / np.sum(self._get_weights(features), axis=1)
        ).flatten()
