import numpy as np
from typing import Union


def epanechnikov_kernel(array):
    return (3 / 4) * (1 - array**2) if np.abs(
        array) <= 1 else 0

def pc_kernel_estimate(coord_dif):
    kernel_func = np.vectorize(epanechnikov_kernel)   
    return kernel_func(coord_dif)


class Regressor:
    _k_neighbours: int
    _metric: str
    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]

    def __init__(self, k: int = 4, 
                 metric: str = "l1"):
        if k <= 0:
            raise ValueError(
                f"invalid k_neighbours value: {k} "
                "k_neighbours could have only positive values"
            )
        if metric != "l1" and metric != "l2":
            raise TypeError(f"Not available metric we support only l1 and l2")
        
        self._metric = metric
        self._k_neighbours = k

    def fit(self, abscissa: np.ndarray,
             ordinates: np.ndarray):
        
        if(not isinstance(abscissa, np.ndarray)):
            raise TypeError("x must be np.array")
        
        if(not isinstance(ordinates, np.ndarray)):
            raise TypeError("y must be np.array")
        
        if abscissa.shape[0] != ordinates.shape[0]:
            raise RuntimeError("You have not filled \
                                abscissa or ordinates")
        
        self._abscissa = abscissa
        self._ordinates = ordinates
    
    def predict(self, abscissa):
        
        if(not isinstance(abscissa, np.ndarray)):
            raise TypeError("y must be np.array")
        
        if(len(abscissa.shape) == 1):
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(
                self._abscissa.shape[0], 1)

        if(self._metric == "l1"):
            dist = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis = 2, ord = 1)
        if(self._metric == "l2"):
            dist = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis = 2)
            
        window_width = np.sort(dist).T[self._k_neighbours]
        
        dist = dist / window_width

        weights = np.where(np.abs(dist).T <= 1, 
                          pc_kernel_estimate(dist), 0)
        
        prediction = np.sum(
            self._ordinates * weights, axis=1)
        
        return prediction / np.sum(weights, axis=1)
        