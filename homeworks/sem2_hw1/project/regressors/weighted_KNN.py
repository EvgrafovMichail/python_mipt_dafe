import numpy as np
from typing import Union, Any
from ast import Slice
from numbers import Real

from regressors.regressor_abc import RegressorABC
from metrics.metric import Metric


K_NEIGHBOURS = 100


class WeightedKNN(RegressorABC):
    _features: np.ndarray[float] = None
    _targets: np.ndarray[Any] = None
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
            _targets = np.ndarray(targets, type=float)
        else:
            _targets = targets
        if _features.shape[0] != _targets.shape[0]:
            count_of_point = np.min(_features.shape[0], _targets.shape[0])
            _features, _targets = _features[:count_of_point], _targets[:count_of_point]

        self._features = _features
        self._targets = _targets

    def predict(
        self, features: Union[Real, Slice]
    ) -> Union[int, np.ndarray[int]]:
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

    def _get_weights(self, features: np.ndarray[float]) -> np.ndarray[float]:
        distances = Metric.get_distances(features, self._features, self._distance)
        window = np.sort(distances, axis=1)[:, self._k_neighbours - 1]
        distances = np.divide(distances, window[..., np.newaxis])

        weights = np.subtract(1, np.power(distances, 2))
        weights[weights < 0] = 0
        weights = np.multiply(0.75, weights)

        return weights

    def _compute_predict(self, features: np.ndarray) -> np.ndarray[int]:
        mask = np.repeat(
            np.unique(self._targets)[..., np.newaxis],
            self._targets.size, axis=1
            ) == self._targets[np.newaxis, ...]
        res = np.multiply(self._get_weights(features)[:, np.newaxis, :], mask[np.newaxis, ...])
        return np.argmax(np.sum(res, axis=2), axis=1).flatten()
