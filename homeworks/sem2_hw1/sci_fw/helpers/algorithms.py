import numpy as np

from sci_fw.enumerations import Metric


def get_distances(
    from_p: np.ndarray,
    to_p: np.ndarray,
    metric: Metric = Metric.EUCLIDEAN
) -> np.ndarray:
    if from_p.shape[-1] != to_p.shape[-1]:
        raise ValueError(
            "Points are not of the same dimension"
        )

    if from_p.ndim == 1:
        from_p = from_p[:, np.newaxis]
        to_p = to_p[:, np.newaxis]

    deltas = from_p[:, np.newaxis, :] - to_p[np.newaxis, :, :]
    if metric == Metric.EUCLIDEAN:
        dists = np.square(deltas)
        dists = np.sum(dists, axis=-1)
        dists = np.sqrt(dists)
    elif metric == Metric.MANHATTAN:
        dists = np.abs(deltas)
        dists = np.sum(dists, axis=-1)
    return dists


def kernel_foreach(
    values: np.ndarray,
    k_neighbours: int
) -> np.ndarray:
    window_reference = (
        k_neighbours if k_neighbours < values.shape[1] else -1
    )
    window_widths = values[:, window_reference]
    kernel_args = values[:, :k_neighbours] / \
        window_widths[:, np.newaxis]
    kernel = 3/4 * (1 - kernel_args ** 2)
    return kernel
