from algorithm.np_regression import NonparametricRegression
from metrics import Metric
from preprocessing import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import os


dir = os.path.dirname(os.path.abspath(__file__))
POINTS_AMOUNT = 10000
BOUNDS = (-10, 10)
FIGSIZE = (8, 8)
K = 400


def _visualize(abscissa, ordinates, predict, save_path):
    _, axis = plt.subplots(1, 1, figsize=FIGSIZE)

    axis.set_title('NonparametricRegression')

    axis.scatter(abscissa, ordinates, label='source', c='cornflowerblue', s=1, alpha=0.5)
    axis.plot(abscissa, predict, label='prediction',
              c='royalblue', linewidth=1.5)

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()

    plt.savefig(save_path)


def test_NPR():
    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = linear_modulated(abscissa)

    regressor = NonparametricRegression(k=K)

    train_X, test_X, train_Y, test_Y = train_test_split(
        abscissa,
        ordinates,
        shuffle=True,
        train_ratio=0.7
    )

    regressor.fit(abscissa, ordinates)
    train_predict = regressor.predict(train_X)
    test_predict = regressor.predict(test_X)

    print(
        f'train_MAE={Metric.MAE(train_Y, train_predict)}',
        f'test_MAE={Metric.MAE(test_Y, test_predict)}',
        f'train_MSE={Metric.MSE(train_Y, train_predict)}',
        f'test_MSE={Metric.MSE(test_Y, test_predict)}',
        f'train_R_2={Metric.R_2(train_Y, train_predict)}',
        f'test_R_2={Metric.R_2(test_Y, test_predict)}',
        sep='\n'
    )

    _visualize(train_X, train_Y, train_predict, save_path=f'{dir}/images/train_NPR')
    _visualize(test_X, test_Y, test_predict, save_path=f'{dir}/images/test_NPR')


def linear(abscissa: np.ndarray) -> np.ndarray:
    function_values = 5 * abscissa + 1
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


def linear_modulated(abscissa: np.ndarray) -> np.ndarray:
    function_values = np.sin(abscissa) * abscissa
    noise = np.random.normal(size=abscissa.size)

    return function_values + noise


if __name__ == "__main__":
    test_NPR()
