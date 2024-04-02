from materials.metrics import Metrics
from typing import Union
import numpy as np
from materials.Errors import (
    ShapeMismatchError,
    NoFitFoundError
)


class KNN:
    _k_neighbours: int
    _points: Union[np.ndarray, None]
    _labels: Union[np.ndarray, None]
    _metric: str

    def __init__(self, k_neighbours: int = 5, metric: str = "l1") -> None:
        if isinstance(k_neighbours, int) and metric in Metrics:
            self._k_neighbours = k_neighbours
            self._points, self._labels = None, None
            self._metric = metric
        else:
            if isinstance(k_neighbours, int):
                raise TypeError('metric from Metric is requred',
                                f'got {metric} instead'
                                )
            elif metric in Metrics:
                raise TypeError("Integer is requred",
                                f'got {k_neighbours} instead'
                                )

    def fit(self, points: np.ndarray, labels: np.ndarray) -> None:
        if (points.shape[0] != labels.shape[0] and points.shape[0] == 0):
            raise ShapeMismatchError(
                f"Features shape {points.shape[0]} != targets shape {labels.shape[0]}",
                "or it has a shape = 0"
            )
        self._points = points
        self._labels = labels

    def predict(self, points: np.ndarray) -> np.ndarray:

        if (self._points is None) or (self._labels is None):
            raise NoFitFoundError("Predict was called before Fit")

        distances = self._distance(points, self._points)

        resulted_indeces = np.argsort(distances, axis=1)[:, :self._k_neighbours]
        resulted_indeces = np.sort(resulted_indeces, axis=1)

        labels_knn = np.tile(self._labels[:], self._k_neighbours)
        points_knn = np.tile(self._points[:], self._k_neighbours)

        resulted_points = points_knn[resulted_indeces.flatten()]
        resulted_points = resulted_points[::, :2]
        resulted_points = resulted_points.reshape(resulted_indeces.shape[0],
                                                  resulted_indeces.shape[1],
                                                  2
                                                  )

        dist_for_core = np.sort(distances, axis=1)[:, :self._k_neighbours]
        dist_for_width_window = np.sort(distances, axis=1)[:, self._k_neighbours - 1]

        dist_for_width_window = np.reshape(dist_for_width_window,
                                           (1,
                                            dist_for_width_window.shape[0])
                                           )
        dist_for_width_window = np.reshape(dist_for_width_window,
                                           (dist_for_width_window.shape[1],
                                            dist_for_width_window.shape[0])
                                           )

        dist_for_width_window = np.tile(dist_for_width_window, self._k_neighbours)
        W = self._core(dist_for_core / dist_for_width_window)

        resulted_labels = labels_knn[resulted_indeces.flatten()]
        resulted_labels = resulted_labels.reshape(resulted_indeces.shape)

        colour_1 = np.sum(resulted_labels * W, 1)  # 1
        colour_0 = np.sum((1 - resulted_labels) * W, 1)  # 0

        resulted_colour = colour_1 > colour_0

        return resulted_colour

    def _distance(self, points_from: np.ndarray, points_to: np.ndarray):
        points_from_extended = np.tile(points_from, points_to.shape[0])
        points_ans = points_from_extended - points_to.flatten()

        if self._metric == Metrics[0]:
            points_ans = points_ans**2

        if self._metric == Metrics[1]:
            points_ans = np.abs(points_ans)

        points_ans = points_ans.reshape(points_from.shape[0], points_to.shape[0], 2)
        distances = np.sum(points_ans, axis=2)
        return distances

    def _core(self, points: np.ndarray):
        weight = 0.75*(1-points**2) * (np.abs(points) <= 1)
        return weight
