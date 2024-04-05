"""Predicator interface.

This module ...
"""

import abc
import numpy as np


class PredicatorABC(metaclass=abc.ABCMeta):
    """
    Predicator Interface.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fit') and 
                callable(subclass.fit) and 
                hasattr(subclass, 'predict') and 
                callable(subclass.predict) or 
                NotImplemented)

    @abc.abstractmethod
    def fit(self, points: np.ndarray, targets: np.ndarray):
        raise NotImplementedError

    @abc.abstractmethod
    def predict(self, points: np.ndarray):
        raise NotImplementedError