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
        axis.scatter(*points, s=60, c="r", marker="x")

    plt.show()


def visualize_images(
    images_normalized: dict[str, np.ndarray]
):
    _, axes = plt.subplots(len(images_normalized), 1, figsize=(16, 9))
    pairs = list(images_normalized.items())
    axes = axes.flatten()

    for i, pair in enumerate(pairs):
        label, image = pair

        axes[i].set_title(label, fontsize=15, fontweight="bold", c="dimgray")
        axes[i].imshow(image.T, cmap="gray")
        axes[i].axis("off")

    plt.show()
