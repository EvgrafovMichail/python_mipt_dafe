import matplotlib.pyplot as plt
import numpy as np


def visualize_image(image: np.ndarray) -> None:
    aspect_ratio = image.shape[0] / image.shape[1]
    side_len = 9

    _, axis = plt.subplots(
        figsize=(side_len, side_len * aspect_ratio)
    )

    axis.imshow(image, cmap="gray")
    axis.axis("off")
    
    plt.show()
