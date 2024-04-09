import numpy as np
from typing import Union


class KNN:
    _k_neighbours: int
    _metric: str
    _points: Union[np.ndarray, None]
    _labels: Union[np.ndarray, None]
    
    def __init__(self, k_neighbours: int = 5, metric: str = "l1") -> None:
        # ваш код  конструктор целое число соседей, предупреждение, валидация >= 0, point labal = none
        if not(metric in ["l1", "l2"]):
            raise TypeError(
                f"Unexpected metric: {metric}"
            )
        
        try:
            if not isinstance(k_neighbours, int):
                k_neighbours = int(k_neighbours)
                print(f'Neighbours count was changed to: {k_neighbours}')

        except TypeError:
            print('Expected integer neighbours count')

        if k_neighbours < 1:
            raise ValueError(
                f'Unexpected neighbours count: {k_neighbours}'
            )
        
        self._metric = metric
        self._k_neighbours = k_neighbours
        self._points = None
        self._labels = None


        
    def fit(self, points: np.ndarray, labels: np.ndarray) -> None:
        # ваш код сохр обуч выборку(копия)
        if len(points) != len(labels):
            raise RuntimeError(
                f'Len doesnt match: {len(points)} != {len(labels)}'
            )
        
        if not(isinstance(points, np.ndarray) and 
               isinstance(labels, np.ndarray)):
            raise TypeError(
                "Unexpected points/labels type"
            )

        self._points = points.copy()
        self._labels = labels.copy()
        
    def predict(self, points: np.ndarray) -> np.ndarray:
        # ваш код только после фит,расст, упорядочить, к ближ

        if not isinstance(points, np.ndarray):
            raise TypeError(
                "Unexpected points type"
            )
        
        if not isinstance(self._points, np.ndarray):
            raise Exception(
                'Expected fit before predict'
            )

        points_from = self._points[np.newaxis, ...]
        points_to = points[:, np.newaxis, :]

        if self._metric == 'l1':
            distances = np.linalg.norm(
                points_from - points_to, axis=2)

        if self._metric == 'l2':
            distances = np.linalg.norm(
                points_from - points_to, axis=2, ord=1)

        h = np.sort(distances)[self._k_neighbours]

        weight = (0.75 * (1 - (np.sort(distances)/h) ** 2)) *\
            (np.abs(np.sort(distances)/h) <= 1)

        mask = np.argsort(distances)
        labels_masked = self._labels[mask]
        labels_k = labels_masked[:, :self._k_neighbours]
        
        weight = weight[:, :self._k_neighbours]

        #в общем суммируем -1, если 0
        #а если 1. то суммируются 1, и знак покажет победителя
        prediction = np.where(
            np.sum((labels_k - 0.5) * 2 * weight, axis=-1) > 0,
            1, 0)
        
        return prediction
    
