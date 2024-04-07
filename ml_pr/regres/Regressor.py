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
        
        h = np.sort(dist).T[self._h]

        kernel = np.where(np.abs(dist.T/h).T <= 1, 
                          pc_kernel_estimate(dist.T/h), 0)

        numerator = np.sum(self._ordinates * kernel, axis=1) / \
            np.sum(kernel, axis=1)

        return numerator

        