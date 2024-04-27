import matplotlib.pyplot as plt
from os.path import isfile
from warnings import warn
import numpy as np

from add_classes.enum_classes import Metric


def find_distances(
        to_find_points: np.ndarray,
        points: np.ndarray,
        metric: Metric,
):
    if len(to_find_points.shape) != len(points.shape):
        to_find_points = to_find_points[:, np.newaxis]

    find_points_dim = to_find_points.shape[-1]
    points = points[:, 0:find_points_dim]

    if metric == Metric.CLASSIC:
        distances = np.sqrt(np.sum((to_find_points[:, np.newaxis] - points) ** 2, axis=2))
    else:
        distances = np.abs(np.sum((to_find_points[:, np.newaxis] - points), axis=2))

    sorted_distances = np.sort(distances, axis=1)

    return (distances, sorted_distances)


def find_kernel(
        to_find_points: np.ndarray,
        points: np.ndarray,
        index_k: int,
        metric: Metric,
) -> np.ndarray:
    distances, sorted_distances = find_distances(to_find_points, points, metric)

    kernel_elem = sorted_distances[::, index_k - 1].reshape(len(sorted_distances), 1)
    kernel_argument = distances / kernel_elem
    kernel = (np.abs(kernel_argument) <= 1) * (0.75 * (1 - kernel_argument ** 2))

    return kernel


def save_file(path_to_save: str) -> None:
    if not (path_to_save == ""):
        path = path_to_save + "/graphic.png"
        if isfile(path):
            warn("Image file graphic.png will be overwritten")
        plt.savefig(path, bbox_inches="tight")


def set_violin(violin_parts) -> None:
    for body in violin_parts["bodies"]:
        body.set_facecolor("cornflowerblue")
        body.set_edgecolor("blue")

    for part in violin_parts:
        if part == "bodies":
            continue

        violin_parts[part].set_edgecolor("cornflowerblue")
