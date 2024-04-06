from numbers import Real
import numpy as np


class ShapeMismatchError(Exception):
    pass


def check_natural(
    n: Real,
    default: int,
    represents: str = "Value"
) -> int:
    if not isinstance(n, int):
        old = n
        n = int(n)
        print(f"{represents} ({old}) has been truncated to an int: {n}")
    if n < 1:
        n = default
        print(f"{represents} is too little, setting to {default} as default")
    return n


def check_array(
    arr: np.ndarray,
    allow_empty: bool = False
) -> np.ndarray:
    arr = np.array(arr)
    if not allow_empty and arr.shape[0] == 0:
        raise ValueError("Input array can't be empty")
    return arr


def check_shapes(
    first: np.ndarray,
    second: np.ndarray,
    raise_exception: bool = True
) -> bool:
    if first.shape[0] == second.shape[0]:
        return True
    if raise_exception:
        raise ShapeMismatchError(
            f"Arrays' shapes don't match"
            f"({first.shape[0]} != {second.shape[0]})"
        )
    return False
