import numpy as np

from algo.regressor import RegressorABC, CallingOrder


def blue_func(x):
    if x == 0:
        return -1
    return 0


def pred_func(x):
    if float(x) > 0:
        return 1
    return 0


class KNN(RegressorABC):

    def __init__(self) -> None:
        self._abscissa_train = None
        self._values = None

    def fit(self, points: np.ndarray, labels: np.ndarray, k: int, metric: str = 'l2') -> None:
        if k <= 0:
            raise ValueError("k_neighbours <= 0")
        if k > len(points):
            raise ValueError("Too many neighbors")

        if metric != 'l2' and metric != 'l1':
            raise ValueError("Metric must be l1 or l2")
        self._metric = metric
        self._k_neighbours = int(k)
        self._abscissa_train = np.array(points.copy())
        self._values = np.array(labels.copy())

    def predict(self, abscissa: np.ndarray) -> np.ndarray:
        if (self._abscissa_train is None) or (self._values is None):
            raise CallingOrder("Predict called earlier than fit")

        # расстояния от каждой точки points до _points
        self._distances = self._dist(abscissa)

        # отбираем только метки первых k соседей для каждой точки
        ind = np.argsort(self._distances)[:, self._k_neighbours-1:self._k_neighbours]
        sliced_matrix = np.take_along_axis(self._distances, ind, axis=-1)
        tmp1 = self.kernel(self._distances / sliced_matrix)

        # расстягиваем массив значений
        label = self._values
        label = label[np.newaxis, :]
        label = np.repeat(label, tmp1.shape[0], axis=0)

        blue = np.vectorize(blue_func)
        blue_label = blue(label)

        v = label + blue_label
        tmp2 = v * tmp1
        pred_values = np.sum(tmp2, axis=-1)  # суммируем значения меток в каждой строке

        pred = np.vectorize(pred_func)

        pred_values = pred(pred_values)

        return pred_values
