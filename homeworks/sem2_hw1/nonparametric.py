import numpy as np
from typing import Union


class nonparametric_regression:
    _k: int
    _metric: str
    _abscissa: Union[np.ndarray, None]
    _ordinates: Union[np.ndarray, None]

    def __init__(
        self,
        k: int = 3,
        metric: str = "l1"
    ) -> None:
        if not(metric in ["l1", "l2"]):
            raise TypeError(
                f"Unexpected metric: {metric}"
            )
        
        try:
            if not isinstance(k, int):
                k = int(k)
                print(f"k was changed to {k}")

        except TypeError:
            print('Unexpected k type')

        if k < 1:
            raise ValueError(
                f'Unexpected k: {k}, expected >= 1'
            )

        self._k = k
        self._metric = metric
        self._abscissa = None
        self._ordinates = None

    def fit(self, abscissa: np.ndarray, ordinata: np.ndarray) -> None:
        # ваш код сохр обуч выборку(копия)
        if len(abscissa) != len(ordinata):
            raise RuntimeError(
                f'Len doesnt match: {len(abscissa)} != {len(ordinata)}'
            )
        
        if not(isinstance(abscissa, np.ndarray) and 
               isinstance(ordinata, np.ndarray)):
            raise TypeError(
                "Unexpected abscissa/ordinates type"
            )

        self._abscissa = abscissa.copy()
        self._ordinates = ordinata.copy()
        
    def predict(self, abscissa: np.ndarray) -> np.ndarray:
        # ваш код только после фит,расст, упорядочить, к ближ

        if not isinstance(abscissa, np.ndarray):
            raise TypeError(
                "Unexpected abscissa type"
            )
        
        if not isinstance(self._abscissa, np.ndarray):
            raise Exception(
                'Expected fit before predict'
            )

        abscissa_from = self._abscissa[np.newaxis, ..., np.newaxis]
        abscissa_to = abscissa[:, np.newaxis, np.newaxis]

        if self._metric == 'l1':
            distances = np.linalg.norm(
                abscissa_from - abscissa_to, axis=2)

        if self._metric == 'l2':
            distances = np.linalg.norm(
                abscissa_from - abscissa_to, axis=2, ord=1)

        h = np.sort(distances)[:, self._k]

        KerE = (0.75 * (1 - (distances/h) ** 2)) *\
            (np.abs(distances/h) <= 1)

        prediction = np.sum(self._ordinates * KerE, axis=-1)/ \
            np.sum(KerE, axis=-1)
        
        print(KerE)

        return prediction
    
