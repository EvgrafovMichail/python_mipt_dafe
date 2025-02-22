from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def visualize_1d(
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    points: Optional[list[tuple[int, int]]] = None,
) -> None:
    _, axis = plt.subplots(figsize=(16, 9))

    axis.plot(abscissa, ordinates, c="royalblue")
    
    shift = 0.05 * (ordinates.max() - ordinates.min())

    axis.set_xlim(np.min(abscissa), np.max(abscissa))
    axis.set_ylim(np.min(ordinates) - shift, np.max(ordinates) + shift)
    axis.grid(True)

    if points:
        points = list(zip(*points))
        axis.scatter(*points, s=80, c="r", marker="x")

    plt.show()


def visualize_lsm(
    abscissa: np.ndarray,
    ordinates_experiment: np.ndarray,
    ordinates_computed: np.ndarray,
) -> None:
    _, axis = plt.subplots(figsize=(16, 9))
    axis: plt.Axes = axis

    axis.scatter(
        abscissa,
        ordinates_experiment,
        c="royalblue",
        s=10,
        alpha=0.6,
        label="experiment",
    )
    axis.plot(
        abscissa,
        ordinates_computed,
        c="royalblue",
        label="lsm",
    )

    axis.set_xlim(np.min(abscissa), np.max(abscissa))
    axis.legend()
    axis.grid()

    plt.show()


def compare_images(image1: np.ndarray, image2: np.ndarray) -> None:
    _, (axis1, axis2) = plt.subplots(1, 2, figsize=(16, 8))
    axis1: plt.Axes = axis1
    axis2: plt.Axes = axis2

    axis1.imshow(image1)
    axis2.imshow(image2)

    axis1.axis("off")
    axis2.axis("off")

    plt.show()
