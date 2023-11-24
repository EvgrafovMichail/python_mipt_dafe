from typing import Iterable, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class RegressorLSM(RegressorABC):
    def fit(self, abscissa: Iterable, ordinates: Iterable) -> None:
        # ваш код
        pass

    def predict(self, abscissa: Union[Real, Iterable]) -> list:
        # ваш код
        return [abscissa] if isinstance(abscissa, Real) else abscissa
