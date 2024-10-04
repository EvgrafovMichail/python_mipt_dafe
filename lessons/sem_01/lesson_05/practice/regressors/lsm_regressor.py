from typing import Sequence, Union
from numbers import Real

from regressors.regressor_abc import RegressorABC


class RegressorLSM(RegressorABC):
    def fit(self, abscissa: Sequence[Real], ordinates: Sequence[Real]) -> None:
        # ваш код
        pass

    def predict(self, abscissa: Union[Real, Sequence[Real]]) -> list:
        # ваш код
        return [abscissa] if isinstance(abscissa, Real) else abscissa
