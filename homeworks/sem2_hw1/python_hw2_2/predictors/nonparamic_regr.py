from typing import Union
import numpy as np


class NR:
    _win_size: int
    _metric: str
    _is_it_fit: bool = False
    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]

    def __init__(self, win_size: int = 4, metric: str = 'l1') -> None:
        if metric != 'l1' and metric != 'l2':
            raise TypeError("wrong metric")
        self._metric = metric
        if not isinstance(win_size, int):
            raise TypeError("not integer")
        if win_size <= 0 or win_size // 1 != win_size:
            print(
                f"your win_size are uncorrect(<0 or not integer)."
                f" We castit into{abs(win_size)//1 + 1}"
            )
            self._win_size = abs(win_size) // 1 + 1

        else:
            self._win_size = win_size

    def fit(self, abscissa: np.ndarray, ordinates: np.ndarray) -> None:
        if abscissa.shape[0] != ordinates.shape[0]:
            raise RuntimeError("different len")
        if isinstance(abscissa, np.ndarray) and isinstance(ordinates, np.ndarray):
            self._abscissa = abscissa
            self._ordinates = ordinates
            self._is_it_fit = True
        else:
            raise TypeError("there is not np.ndarray")

    def predict(
            self,
            abscissa: np.ndarray,
    ):
        if not self._is_it_fit:
            raise RuntimeError("There are no test data")
        if not isinstance(abscissa, np.ndarray):
            raise TypeError("not np.array")
        if len(abscissa.shape) == 1:  # нам в л.бом случае наужен двумерный массив координат
            abscissa = abscissa.reshape(abscissa.shape[0], 1)
            self._abscissa = self._abscissa.reshape(self._abscissa.shape[0], 1)
        if self._metric == 'l1':
            distances = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis=2)
        if self._metric == 'l2':
            distances = np.linalg.norm(
                self._abscissa - abscissa[:, np.newaxis], axis=2, ord=1)

        k_windows = np.sort(distances).T[self._win_size]

        kerE = np.where(np.abs(distances.T / k_windows).T <= 1,
                        0.75 * (1 - (distances.T / k_windows).T**2), 0)
        approach = np.sum(self._ordinates * kerE, axis=1) / \
            np.sum(kerE, axis=1)
        return approach
