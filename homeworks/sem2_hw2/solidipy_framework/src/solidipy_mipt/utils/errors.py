"""All exist errors for solidipy_mipt framework."""

from typing import TypeAlias

ShapeType: TypeAlias = tuple[int]


class ShapeMismatchError(Exception):
    """
    Exception raised when shapes of arrays do not match.

    This exception is raised when performing operations that require
    arrays to have compatible shapes, but the shapes provided
    are not suitable for the operation.

    Attributes:
        message: Explanation of the error.
        shapes: The mismatched shapes causing the error.

    Example:
        >>> import numpy as np
        >>> from solidipy_mipt.utils.errors import ShapeMismatchError
        >>> a = np.array([[1, 2], [3, 4]])
        >>> b = np.array([1, 2, 3, 4])
        >>> try:
        ...     if a.shape != b.shape:
        ...         raise ShapeMismatchError("Shapes do not match", (a.shape, b.shape))
        ... except ShapeMismatchError as e:
        ...     print(f"ShapeMismatchError: {e.message}")
        ...     print(f"Mismatched shapes: {e.shapes}")
        ShapeMismatchError: Shapes do not match
        Mismatched shapes: ((2, 2), (4,))
    """
    def __init__(
        self,
        message: str,
        shapes: tuple[ShapeType]
    ):
        """
        Initialize the ShapeMismatchError with a message and the mismatched shapes.

        Args:
            message: Explanation of the error.
            shapes: The shapes causing the error.
        """
        super().__init__(message)
        self.message = message
        self.shapes = shapes


class UntrainedModelError(Exception):
    """
    Exception raised when use untrained model.

    Attributes:
        base_message: The base message.
        message: Explanation of the error.
        model_name: The untrained model causing the error.

    Example:
        >>> import numpy as np
        >>> from solidipy_mipt.algorithms import WKNN
        >>> from solidipy_mipt.utils.errors import UntrainedModelError
        >>> X_test = np.array([[1, 2], [3, 4]])
        >>> wknn = WKNN()
        >>> try:
        ...     wknn.predict(X_test)
        ... except UntrainedModelError as e:
        ...     print(f"UntrainedModelError: {e.message}")
        ...     print(f"Model name: {e.model_name}")
        UntrainedModelError: Use untrained model.
        Model name: WKNN
    """

    base_message = "Use untrained model. "

    def __init__(
        self,
        message: str,
        model_name: str
    ):
        """
        Initialize the UntrainedModelError with a message and the model name.

        Args:
            message: Explanation of the error.
            model_name: The untrained model causing the error.
        """
        super().__init__(message)
        self.message = self.base_message + message
        self.shapes = model_name
