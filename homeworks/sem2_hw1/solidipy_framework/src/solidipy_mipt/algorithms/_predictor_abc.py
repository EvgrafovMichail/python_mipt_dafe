"""Predictor interface."""

import abc
import numpy as np


class PredictorABC(metaclass=abc.ABCMeta):
    """
    Abstract base class for predictors.

    This class defines the interface that all predictors should implement.

    Methods:
        fit(X, y): Train the predictor using input data `X` and target `y`.
        predict(X): Predict the target variable for input data `X`.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'fit') and
                callable(subclass.fit) and
                hasattr(subclass, 'predict') and
                callable(subclass.predict) or
                NotImplemented)

    @abc.abstractmethod
    def fit(
        self, X: np.ndarray,
        y: np.ndarray
    ) -> None:
        """
        Train the predictor using input data `X` and target `y`.

        This method should implement the training logic of the predictor.

        Args:
            X: Input `X` or training data.
            y: Target variable or labels.

        Returns:
            None
        """

        raise NotImplementedError

    @abc.abstractmethod
    def predict(
        self,
        X: np.ndarray
    ) -> np.ndarray:
        """
        Predict the target variable for input data `X`.

        This method should generate predictions for the input data `X`.

        Args:
            X: Input `X` or data to make predictions on.

        Returns:
            array-like: Predicted target variable or labels.
        """
        raise NotImplementedError
