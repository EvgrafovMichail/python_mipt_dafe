import numpy as np
import cv2 as cv


def read_grayscale_image(path_to_image: str) -> np.ndarray:
    image = cv.imread(path_to_image)
    image = cv.cvtColor(image, code=cv.COLOR_BGR2GRAY)

    return image
