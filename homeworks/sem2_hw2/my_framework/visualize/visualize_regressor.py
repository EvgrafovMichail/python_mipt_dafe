import matplotlib.pyplot as plt
import numpy as np

FIGSIZE = (16, 9)


def visualize_regressor(
    abscissa: np.ndarray,
    ordinates: np.ndarray,
    predictions: np.ndarray,
    error: np.ndarray
) -> None:
    _, axis = plt.subplots(figsize=FIGSIZE)
    axis.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)
    axis.plot(abscissa, predictions, label='prediction', c='steelblue')
    axis.plot(abscissa, predictions - error, label='error',linestyle='--',c="red")
    axis.plot(abscissa, predictions + error,linestyle='--',c="red")
    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()

    plt.show()

