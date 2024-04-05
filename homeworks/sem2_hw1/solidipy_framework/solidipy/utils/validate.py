"""Validating data.

This module ...

Example:
    from solidipy.utils.validate import check_size

    
    check_size(arr_1, arr_2, axis=(0, ), min_shapes_count=0) # May throw exception!
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
        arr_1: 
        arr_2:
        axis:
        min_shapes_count:
    
    Returns:
        None. This function can throw ValueError or ShapeMismatchError.
    """

    axis = (int(ax) for ax in axis)
    shapes_count = min(len(arr_1.shape), len(arr_2.shape))

    for ax in axis:
        if not (-1 <= ax < shapes_count):
            raise ValueError("bad axis") # TODO bad message

        if arr_1.shape[ax] != arr_2.shape[ax]:
            print(f"1: {arr_1.shape[ax]} 2: {arr_2.shape[ax]}")
            raise ShapeMismatchError()

    if shapes_count < min_shapes_count:
        raise ValueError() # TODO add custom error