from solidipy_mipt import mse, mae, dc, train_test_split
from solidipy_mipt.algorithms import NonparametricRegressor

import matplotlib.pyplot as plt
import numpy as np

POINTS_AMOUNT = 102
BOUNDS = (0, 20)
FIGSIZE = (16, 9)


def visualize_results(
    abscissa: list,
    ordinates: list,
    predictions: list,
) -> None:
    _, axis = plt.subplots(figsize=FIGSIZE)
    axis.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)
    axis.plot(abscissa, predictions, label='prediction', c='steelblue')

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()

    plt.show()


def start() -> None:
    np_regressor = NonparametricRegressor()

    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT).reshape((POINTS_AMOUNT, 1))
    ordinates = np.sqrt(abscissa)

    print(abscissa, ordinates, sep="\n\n", end="\n\n")

    X_train, X_test, y_train, y_test = train_test_split(abscissa, ordinates, shuffle=True)
    print(X_train, y_train, sep="\n\n")

    np_regressor.fit(X_train, y_train)

    predictions = np_regressor.predict(X_test)
    visualize_results(abscissa, ordinates, predictions)
    print(mse(predictions, y_test), mae(predictions, y_test), dc(predictions, y_test))


if __name__ == "__main__":
    start()
