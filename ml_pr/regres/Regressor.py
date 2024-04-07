import numpy as np
from typing import Union

def epanechnikov_kernel(array):

    if abs(array) <= 1:
        return 3/4 * (1 - array**2)
    else:
        return 0


def pc_kernel_estimate(coord_dif):
    kernel_func = np.vectorize(epanechnikov_kernel)
    
    return kernel_func(coord_dif)


class Regressor:
    _h: int
    _metric: str
    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]

    def __init__(self, h: int = 4, 
                 metric: str = "l1"):
        if h <= 0:
            raise ValueError(
                f"invalid k_neighbours value: {h} "
                "k_neighbours could have only positive values"
            )
        self._metric = metric
        self._h = h

    def fit(self, abscissa: np.ndarray,
             ordinates: np.ndarray):
        self._abscissa = abscissa
        self._ordinates = ordinates
    
    def predict(self, abscissa):
        if(len(abscissa.shape) == 1):
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(
                self._abscissa.shape[0], 1)

        if(self._metric == "l1"):
            dist = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis = 2)
        if(self._metric == "l2"):
            dist = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis = 2, ord = 1)
            
        window_width = np.sort(dist).T[self._h - 1]
        dist = dist / window_width

        weights = np.where(np.abs(dist).T <= 1, 
                          pc_kernel_estimate(dist), 0)
        
        prediction = np.sum(
            self._ordinates * weights, axis=1)
        
        return prediction / np.sum(weights, axis=1)
        