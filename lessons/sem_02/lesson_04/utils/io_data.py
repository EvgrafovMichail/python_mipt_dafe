import cv2 as cv
import numpy as np


def get_image(path_to_image: str) -> np.ndarray:
    image = cv.imread(path_to_image)
    return cv.cvtColor(image, code=cv.COLOR_BGR2RGB)
