import numpy as np
import matplotlib.pyplot as plt
from NonparametricRegression.nonparametric_regression import NR
from utils.random_seed import freeze_random_seed
from utils.quality_control import print_estimation


def generate_ordinates(abscissa, function, noise):
    rng = np.random.default_rng(42)     # шум: умножает (от 1 - noise) до (1 + nose)
    return function(abscissa) * (1 + (rng.random((abscissa.shape[0])) - 0.5) * noise * 2)


def show(abscissa, ordinates, prediction):
    plt.scatter(abscissa, ordinates, label='input data', c='#5353ff', s=1)
    plt.plot(abscissa, prediction, label=prediction, c="#ff3131")
    plt.legend(["input data", "prediction"])
    plt.show()


def func(x):
    return 69 * x + 228


def main():
    freeze_random_seed()
    dist_index = 7
    metric = "l2"
    n_abscissa = 1337
    function = func
    np.vectorize(function)
    noise = 0.1

    x = np.arange(n_abscissa)
    y = generate_ordinates(x, function, noise)
    regression = NR(dist_index, metric)
    regression.fit(x, y)
    prediction = regression.predict(x)

    print_estimation(prediction, y)
    show(x, y, prediction)


main()
