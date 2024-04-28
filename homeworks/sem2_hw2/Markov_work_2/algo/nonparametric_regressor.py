import numpy as np

from algo.regressor import RegressorABC, CallingOrder


class NonparametricRegressor(RegressorABC):

    def __init__(self) -> None:
        self._abscissa_train = None
        self._values = None

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray, k: int, metric: str = 'l2') -> None:
        if metric != 'l2' and metric != 'l1':
            raise ValueError("Metric must be l1 or l2")

        if k <= 0:
            raise ValueError("k_neighbours <= 0")
        if k > len(abscissa):
            raise ValueError("Too many neighbors")

        self._k_neighbours = k
        self._metric = metric
        self._abscissa_train = np.array(abscissa.copy())
        self._values = np.array(ordinates.copy())

    def predict(self, abscissa: np.ndarray) -> np.ndarray:
        if (self._abscissa_train is None) or (self._values is None):
            raise CallingOrder("Predict called earlier than fit")

        self._distances = self._dist(abscissa)

        # расчет ширины окна
        ind = np.argsort(self._distances)[:, self._k_neighbours-1:self._k_neighbours]
        sliced_matrix = np.take_along_axis(self._distances, ind, axis=-1)

        tmp1 = self.kernel(self._distances / sliced_matrix)

        # расстягиваем массив значений
        values = self._values[np.newaxis, :]
        values = np.repeat(values, tmp1.shape[0], axis=0)

        tmp2 = values * tmp1
        tmp2 = np.sum(tmp2, axis=-1) / np.sum(tmp1, axis=-1)
        tmp2 = tmp2.flatten()
        res = tmp2

        return res
