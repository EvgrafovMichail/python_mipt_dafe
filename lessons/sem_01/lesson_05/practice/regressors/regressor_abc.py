import abc

from typing import Sequence, Union
from numbers import Real


class RegressorABC(abc.ABC):
    """
    Интерфейс регрессора.
    """

    @abc.abstractmethod
    def fit(self, abscissa: Sequence[Real], ordinates: Sequence[Real]) -> None:
        """
        Обучает регрессор, используя данные обучающей выборки.

        Args:
            abscissa: последовательность абсцисс точек.
            ordinates: последовательность ординат точек.
        """
        ...

    @abc.abstractmethod
    def predict(
        self, abscissa: Union[Real, Sequence[Real]]
    ) -> list[Real]:
        """
        Аппроксимирует значение функции в переданных точках.

        Args:
            abscissa: число - одна точка, или последовательность точек,
                в которых необходимо аппроксимировать значение функции.

        Returns:
            Список аппроксимаций.

        Raises:
            RuntimeError, если predict вызван до вызова fit.
        """
        ...
