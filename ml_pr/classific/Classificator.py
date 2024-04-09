import numpy as np
from typing import Union
import math

def epanechnikov_kernel(array):
    return (3 / 4) * (1 - array**2) if np.abs(
        array) <= 1 else 0


def pc_kernel_estimate(coord_dif):
    kernel_func = np.vectorize(epanechnikov_kernel)
    return kernel_func(coord_dif)

class Classificator:
    _k_neighbours: int
    _win_h: int
    _points: Union[np.ndarray, None]
    _labels: Union[np.ndarray, None]
    _metric: str
    
    def __init__(self, 
                 win_size = 4, 
                 k_neighbours = 7, 
                 metric = "l1") -> None:
        
        self._k_neighbours = k_neighbours
        self._points = None
        self._labels = None
        self._metric = metric
        self._win_h = win_size
    
    def fit(self, points: np.ndarray, labels: np.ndarray) -> None:
        self._points = points
        self._labels = labels

        
    def predict(self, points: np.ndarray):

        train_points = np.repeat(self._points[np.newaxis, :, :], 
                                 points.shape[0], 
                                 axis=0)
        new_points = np.repeat(points[:, np.newaxis, :], 
                               self._points.shape[0], 
                               axis=1)
        
        difference = train_points - new_points
        
        if(self._metric == "l1"):
            dist = np.linalg.norm(
                difference, axis = 2, ord = 1)
        if(self._metric == "l2"):
            dist = np.linalg.norm(
                difference, axis = 2)
            
        sort_dist = np.sort(dist)

        h_windows = sort_dist.T[self._k_neighbours]

        h_windows = h_windows.reshape(h_windows.shape[0], 1)

        weights = pc_kernel_estimate(sort_dist / h_windows
                                     )[::, 0:self._k_neighbours]

        labels = self._labels[np.argsort(dist)][::, 0:self._k_neighbours]

        return np.where(((labels - 0.5) * weights).sum(axis=1)
                         > 0, 1, 0)


