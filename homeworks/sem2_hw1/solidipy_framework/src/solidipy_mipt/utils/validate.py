"""Validating data.

This module contain methods to validate data.
"""

import numpy as np

from typing import Iterable
from .errors import ShapeMismatchError


def check_size(
        arr_1: np.ndarray,
        arr_2: np.ndarray,
        axis: Iterable[int] = (0, ),
        min_shapes_count: int = 0
) -> None:
    """
    Check equality of sizes for given arrays.

    Args:
        arr_1: First array.
        arr_2: Second array.
        axis: Axes along which comparison will be made.
        min_shapes_count: Minimum number of array axes.

    Returns:
        None

    Raises:
        ShapeMismatchError: If first and second array shapes mismatch.
        ValueError: If given axis does not match array shapes.
        ValueError: If array shapes are less than given min_shapes_count.
    """

    axis = (int(ax) for ax in axis)
    shapes_count = min(len(arr_1.shape), len(arr_2.shape))

    for ax in axis:
        if not (-1 <= ax < shapes_count):
            raise ValueError(
                "Given axis does not match array shapes. "
                f"Maximum axis number: {shapes_count}."
            )

        if arr_1.shape[ax] != arr_2.shape[ax]:
            raise ShapeMismatchError(
                "Shapes do not match", (arr_1.shape, arr_2.shape)
            )

    if shapes_count < min_shapes_count:
        raise ValueError(
            "Array shapes are less than given min_shapes_count: "
            f"array_{shapes_count=} {min_shapes_count=}."
        )
