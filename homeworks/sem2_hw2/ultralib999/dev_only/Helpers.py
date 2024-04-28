import numpy as np
import matplotlib.pyplot as plt
from ultralib999.GlobalVars import DiagramTypes, DEFAULT_FILE_SAVE_NAME
import os
import warnings


class ShapeMismatchError(Exception):
    pass


def _could_be_compared(x: np.ndarray, y: np.ndarray) -> None:
    if not (isinstance(x, np.ndarray) and isinstance(y, np.ndarray)):
        raise ValueError(f"Expected numpy.ndarray, got: {type(x)}, {type(y)}")
    if x.shape[0] != y.shape[0] and y.size != 0:
        raise IndexError(f"two arrays must have the same "
                         f"non-zero length, got: {x.shape[0]} {y.shape[0]}")


def _draw_by_type(
        axis: plt.Axes,
        diagram_type: str,
        data: np.ndarray,
        do_vert=True,
        value: int = 1
) -> None:
    if diagram_type == DiagramTypes.VIOLIN:
        axis.violinplot(
            data,
            showmedians=True,
            vert=do_vert,
        )

    elif diagram_type == DiagramTypes.HIST:
        axis.hist(
            data,
            density=True,
            color="cornflowerblue",
            orientation="vertical" if do_vert else "horizontal",
            alpha=0.5,
            bins=50
        )
    else:
        axis.boxplot(
            data,
            vert=do_vert,
        )
    axis.set_xlabel("dim: " + str(value), fontdict=dict(weight='bold', color='red'))


def _save_pic(path_to_save: str) -> None:
    # path processing
    if path_to_save != "":
        # check is it folder and does it really exists
        if os.path.isdir(path_to_save):
            path_to_save += DEFAULT_FILE_SAVE_NAME

        if os.path.isfile(path_to_save):
            warnings.warn("File with this name already exists.")

    if path_to_save != "":
        plt.savefig(path_to_save, bbox_inches="tight")
    plt.show()


def _check_dims(arr: np.ndarray, dim: int, fname: str) -> None:
    if not isinstance(arr, np.ndarray):
        raise TypeError(f"{fname} must be np.ndarray, got: {type(arr)}")

    if (len(arr.shape) != 1 and arr.shape[1] != dim) or (len(arr.shape) == 1 and dim != 1):
        raise ShapeMismatchError(f"{fname} must be {dim}D array, got shape: {arr.shape}")

    # если одномерный - вытягиваем в столб
    if len(arr.shape) == 1:
        return arr.reshape(arr.shape[0], 1)
    return None


def _default_vis_check(axis: np.ndarray, path: str, enable_lists: bool = False):
    if not isinstance(path, str):
        raise TypeError(f"path_to_save must be str, got: {type(path)}")

    if enable_lists:
        if not isinstance(axis, plt.Axes):
            if not isinstance(axis, list) or any([not isinstance(i, plt.Axes) for i in axis]):
                raise TypeError(f"axis must be plt.Axes or list[plt.Axes], got: {type(axis)}")
    else:
        if not isinstance(axis, plt.Axes):
            raise TypeError(f"axis must be plt.Axes, got: {type(axis)}")
