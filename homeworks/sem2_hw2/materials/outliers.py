import numpy as np
from typing import (
    Callable, Any, Optional
)


def get_boxplot_outliers(
    data: np.ndarray,
    key: Optional[Callable[[Any], Any]] = None,
) -> np.ndarray:

    cr_data = data.copy()

    if key:
        if not callable(key):
            raise TypeError(
                "Unknown input for key: supposed to be a function"
            )

        cr_data = cr_data[np.argsort(cr_data, axis=0, key=key(cr_data))]
    else:
        cr_data = np.sort(cr_data, axis=0)

    q1 = cr_data[int(0.25*np.size(cr_data, axis=0))]
    q3 = cr_data[int(0.75*np.size(cr_data, axis=0))]
    epsilon = (q3 - q1) * 1.5

    mask_low = cr_data < (q1 - epsilon)
    mask_high = cr_data > (q3 + epsilon)
    mask = mask_high + mask_low

    if cr_data.shape[1] > 1:
        mask = np.prod(mask, 1)

    return np.where(mask != 0)
