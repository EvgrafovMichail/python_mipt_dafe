import numpy as np
from typing import Union
import math



class Classificator:
    _k_neighbours: int
    _points: Union[np.ndarray, None]
    _labels: Union[np.ndarray, None]
    _metric: str
    
    def __init__(self, k_neighbours = 7, metric = "l1") -> None:
        self._k_neighbours = k_neighbours
        self._points = None
        self._labels = None
        self._metric = metric
    
    def fit(self, points: np.ndarray, labels: np.ndarray) -> None:
        self._points = points
        self._labels = labels
        
    def predict(self, points: np.ndarray):
        got_x, got_y = points[:, 1], points[:, 0]
        test_x, test_y = self._points[:, 1], self._points[:, 0]
        test_y = test_y.reshape(test_y.shape[0], 1)
        test_x = test_x.reshape(test_x.shape[0], 1)
        
        if(self._metric == "l1"):
            y_diff = np.abs(got_y - test_y)
            x_diff = np.abs(got_x - test_x)
        else:
            y_diff = np.power(got_y - test_y, 2)
            x_diff = np.power(got_x - test_x, 2)
        
        predicted_points = x_diff + y_diff
        
        indexes = predicted_points.argsort(axis=0)
        indexes = indexes[:self._k_neighbours, :]
        
        indexes_to_labels = np.vectorize(lambda x: self._labels[x])
        res = np.vectorize(lambda el: round(el))(np.mean(indexes_to_labels(indexes), axis=0))
        return res

