from solidipy_mipt import mse, mae, dc, train_test_split
from solidipy_mipt.algorithms import NonparametricRegressor

import matplotlib.pyplot as plt
import numpy as np

POINTS_AMOUNT = 100
BOUNDS = (0, 5)
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
    
    abscissa = np.linspace(*BOUNDS, POINTS_AMOUNT)
    ordinates = abscissa ** 2

    abscissa = abscissa.reshape((POINTS_AMOUNT, 1))

    X_train, X_test, y_train, y_test = train_test_split(abscissa, ordinates, train_ratio=0.8, shuffle=True)

    np_regressor.fit(X_train, y_train + np.random.random(y_train.shape[0]) * np.random.randint(-1, 2, y_train.shape[0]))

    prediction = np_regressor.predict(X_test)

    indeces = np.argsort(np.sum(X_test, axis=-1))
    X_test = X_test[indeces]
    y_test = y_test[indeces]
    prediction = prediction[indeces]

    visualize_results(X_test, y_test, prediction)
    print(mse(prediction, y_test), mae(prediction, y_test), dc(prediction, y_test))


if __name__ == "__main__":
    start()
