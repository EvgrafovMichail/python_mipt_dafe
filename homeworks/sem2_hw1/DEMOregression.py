import numpy as np
import matplotlib.pyplot as plt
from typing import Optional
from Algorithms import NR
from utils.random_seed import freeze_random_seed
from utils.quality_control import print_estimation
from utils.models import RegressionVisualizeSettings

DIST_INDEX = 7
METRIC = "l2"
N_ABSCISSA = 1337

def generate_ordinates(abscissa, function, noise):
    rng = np.random.default_rng(42)     # шум: умножает (от 1 - noise) до (1 + nose)
    return function(abscissa) * (1 + (rng.random((abscissa.shape[0])) - 0.5) * noise * 2)


def show(
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    prediction: np.ndarray,
    error: Optional[list[np.ndarray]] = None,
    settings: RegressionVisualizeSettings = RegressionVisualizeSettings()
):
    plt.scatter(abscissa, ordinates, label='input data', c=settings._points_color, s=settings._points_size)
    plt.plot(abscissa, prediction, label='prediction', c=settings._prediction_color)
    if (error is not None):
        plt.plot(abscissa, error, label = 'error', c=settings.error_color, linestyle=settings.error_linestyle)
    plt.legend(["input data", "prediction"])
    plt.show()


def func(x):
    return 5 * x + 3


def main():
    freeze_random_seed()
    function = func
    np.vectorize(function)
    noise = 0.1

    x = np.arange(N_ABSCISSA)
    y = generate_ordinates(x, function, noise)
    regression = NR(DIST_INDEX, METRIC)
    regression.fit(x, y)
    prediction = regression.predict(x)

    print_estimation(prediction, y)
    show(x, y, prediction)


main()
