import numpy as np


def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)
    ordinates = function_values + noise
    points = np.hstack((abscissa[:, np.newaxis], ordinates[:, np.newaxis]))

    return points


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)
    ordinates = function_values + noise
    points = np.hstack((abscissa[:, np.newaxis], ordinates[:, np.newaxis]))

    return points
