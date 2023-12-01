from typing import Iterable, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class RegressorLSM(RegressorABC):
    _incline: float = None
    _shift: float = None
    _abscissa: list = []
    _ordinates: list = []


    def fit(self, abscissa: Iterable, ordinates: Iterable) -> None:
        self._abscissa = list(abscissa)
        self._ordinates = list(ordinates)
        self._compute_parametrs(abscissa, ordinates)

    

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
            predictions.append(abs_i * self._incline + self._shift)
        
        return predictions
    

    def _compute_parametrs(self, abscissa: Iterable, ordinates: Iterable) -> None:
        amount_points = len(abscissa)
        x_average = sum(abscissa) / amount_points
        x_squres_average = sum(i ** 2 for i in abscissa) / amount_points
        y_average = sum(ordinates) / amount_points
        xy_average = sum(abscissa[i] * ordinates[i] for i in range(amount_points)) / amount_points

        incline = (xy_average - x_average * y_average) / (x_squres_average - x_average ** 2)
        shift = y_average - incline * x_average

        self._incline=incline
        self._shift=shift
