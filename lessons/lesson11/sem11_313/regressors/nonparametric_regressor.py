from turtle import window_width
from typing import Iterable, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


K_NEIGHBOURS = 100

class NonparametricRegressor(RegressorABC):
    _abscissa: list = []
    _ordinates: list = []
    _k_neighbours: int = K_NEIGHBOURS
    
    def __init__(self, k_neighbours: int = K_NEIGHBOURS) -> None:
        k_neighbours = int(k_neighbours)

        if k_neighbours <= 0:
            raise ValueError(
                f'invalid k_neighbours value: {k_neighbours}'
                'k_neighbours could have only positive values;'
            )
        
        self._k_neighbours = k_neighbours


    def fit(self, abscissa: Iterable, ordinates: Iterable) -> None:
        self._abscissa = list(abscissa)
        self._ordinates = list(ordinates)


    def predict(self, abscissa: Union[Real, Iterable]) -> list:
        if not self._abscissa or not self._ordinates:
            raise RuntimeError(
                'method fit() should be called before predict():'
            )
        
        if isinstance(abscissa, Real):
            abscissa = [abscissa]
        else:
            abscissa = list(abscissa)

        predictions = []
        for abs_i in abscissa:
            weights = self._get_weights(abs_i)
            predictions.append(self._compute_prediction(weights))

        return predictions

    def _get_weights(self, abscissa: float) -> list[float]:
        distances = [abs(abscissa - x_i) for x_i in self._abscissa]
        window = sorted(distances)[self._k_neighbours - 1]
        distances = [distance / window for distance in distances]

        weights = [
            0.75 * (1 - dist ** 2) if dist <= 1 else 0
            for dist in distances
        ]

        return weights
    
    def _compute_prediction(self, weights: list[float]) -> float:
        prediction = sum(weight * y for weight, y in zip(weights, self._ordinates))

        return prediction / sum(weights)
