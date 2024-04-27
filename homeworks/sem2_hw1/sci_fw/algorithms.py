import numpy as np
from typing import Union

from sci_fw.helpers.data import check_array, check_shapes, check_natural
from sci_fw.helpers.algorithms import get_distances, kernel_foreach
from sci_fw.enumerations import Metric

K_NEIGHBOURS = 5


class NonparametricRegressor:
    _k_neighbours: int
    _metric: Metric
    _abscissa: Union[np.ndarray, None]
    _ordinate: Union[np.ndarray, None]

    def __init__(self, k_neighbours: int = K_NEIGHBOURS, metric: Metric = Metric.EUCLIDEAN) -> None:
        self._k_neighbours = check_natural(
            k_neighbours, K_NEIGHBOURS, "Number of neighbours")
        self._metric = Metric(metric)
        self._abscissa = None
        self._ordinate = None

    def fit(self, abscissa: np.ndarray, ordinate: np.ndarray) -> None:
        abscissa = check_array(abscissa)
        ordinate = check_array(ordinate)
        check_shapes(abscissa, ordinate)

        self._abscissa = abscissa
        self._ordinate = ordinate

    def predict(self, points: np.ndarray) -> np.ndarray:
        if self._abscissa is None or self._ordinate is None:
            raise RuntimeError("Use 'fit' before 'predict'")
        points = check_array(points)

        dists = get_distances(points, self._abscissa, self._metric)

        # sort known points and corresponding ordinates by distance
        ind_sorted = np.argsort(dists)
        dists = np.take_along_axis(dists, ind_sorted, axis=-1)
        ordinates = np.tile(self._ordinate, (dists.shape[0], 1))
        ordinates = np.take_along_axis(
            ordinates, ind_sorted, axis=-1
        )[:, :self._k_neighbours]

        # calculate weight for each point
        weights = kernel_foreach(dists, self._k_neighbours)

        # get prediction
        predicted_ordinate = np.sum(weights * ordinates, axis=-1)
        predicted_ordinate /= np.sum(weights, axis=-1)
        return predicted_ordinate


class KNN:
    _k_neighbours: int
    _metric: Metric
    _points: Union[np.ndarray, None]
    _labels: Union[np.ndarray, None]

    def __init__(self, k_neighbours: int = K_NEIGHBOURS, metric: Metric = Metric.EUCLIDEAN) -> None:
        self._k_neighbours = check_natural(
            k_neighbours, K_NEIGHBOURS, "Number of neighbours")
        self._metric = Metric(metric)
        self._points = None
        self._labels = None

    def fit(self, points: np.ndarray, labels: np.ndarray) -> None:
        points = check_array(points)
        labels = check_array(labels)
        check_shapes(points, labels)

        self._points = points
        self._labels = labels

    def predict(self, points: np.ndarray) -> np.ndarray:
        if self._points is None or self._labels is None:
            raise RuntimeError("Use 'fit' before 'predict'")
        points = check_array(points)

        dists = get_distances(points, self._points, metric=self._metric)

        # sort known points and corresponding labels by distance
        ind_sorted = np.argsort(dists)
        dists = np.take_along_axis(
            dists, ind_sorted, axis=-1)
        res_labels = np.tile(self._labels, (dists.shape[0], 1))
        res_labels = np.take_along_axis(
            res_labels, ind_sorted, axis=-1)[:, :self._k_neighbours]

        # calculate weight for each label
        label_weights = kernel_foreach(dists, self._k_neighbours)

        # get prediction
        res_labels_with_weights = np.concatenate(
            (res_labels, label_weights), axis=-1)
        res_labels = np.apply_along_axis(
            lambda slice: np.bincount(
                slice[:self._k_neighbours].astype(int),
                weights=slice[self._k_neighbours:]).argmax(),
            arr=res_labels_with_weights,
            axis=1
        )
        return res_labels
