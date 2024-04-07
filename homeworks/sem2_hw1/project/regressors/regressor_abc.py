import abc
import numpy as np

from typing import Iterable, Union
from numbers import Real


class RegressorABC(abc.ABC):
    @abc.abstractmethod
    def fit(self, abscissa: Iterable, ordinates: Iterable) -> None:
        ...

    @abc.abstractmethod
    def predict(
        self, abscissa: Union[Real, Iterable]
    ) -> np.ndarray:
        ...
