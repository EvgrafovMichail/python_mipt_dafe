import numpy as np
import visualize_distribution
from visualize_distribution import visualize_distribution
from preprocessing.get_boxplot_outliers import get_boxplot_outliers


x = np.array([
    ["mama", "apapa", 'rr'],
    ["a", "z", "o"],
    ["aeeeeeeeeeeeee", "e", "o"]
])

"""key = max
print(x[np.apply_along_axis(key, 1, x).argsort()])"""

print(get_boxplot_outliers(x, min, 1))

def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any] = "quicksort",
) -> np.ndarray:
    if not (isinstance(data, np.ndarray)):
        raise ValueError("data must be a np.ndarray")

    keys = ["quicksort", "mergesort", "heapsort", "stable"]
    if not (key in keys):
        raise ValueError(f"{key} doesn't exist")

    indexes_sorted = np.argsort(data, kind=key, axis=0)
    data_sorted = np.sort(data, kind=key, axis=0)

    # abscissa
    abscissa_indexes_sorted = indexes_sorted[::, 0]
    abscissa_sorted = data_sorted[::, 0]

    abscissa_quartile1 = int(abscissa_sorted[int(len(abscissa_sorted) * 0.25)])
    abscissa_quartile3 = int(abscissa_sorted[int(len(abscissa_sorted) * 0.75)])
    abscissa_epsilon = int((abscissa_quartile3 - abscissa_quartile1) * 1.5)

    abscissa_lower = abscissa_sorted < abscissa_quartile1 - abscissa_epsilon
    abscissa_upper = abscissa_sorted > abscissa_quartile3 + abscissa_epsilon

    abscissa_indexes_cut = np.append(
        abscissa_indexes_sorted[abscissa_lower],
        abscissa_indexes_sorted[abscissa_upper],
    )

    # ordinates
    ordinates_indexes_sorted = indexes_sorted[::, 1]
    ordinates_sorted = data_sorted[::, 1]

    ordinates_quartile1 = round(ordinates_sorted[int(len(ordinates_sorted) * 0.25)])
    ordinates_quartile3 = round(ordinates_sorted[int(len(ordinates_sorted) * 0.75)])
    ordinates_epsilon = int((ordinates_quartile3 - ordinates_quartile1) * 1.5)

    ordinates_lower = ordinates_sorted < ordinates_quartile1 - ordinates_epsilon
    ordinates_upper = ordinates_sorted > ordinates_quartile3 + ordinates_epsilon

    ordinates_indexes_cut = np.append(
        ordinates_indexes_sorted[ordinates_lower],
        ordinates_indexes_sorted[ordinates_upper],
    )

    return abscissa_indexes_cut, ordinates_indexes_cut



def get_boxplot_outliers(
    data: np.ndarray,
    key: Callable[[Any], Any],
) -> np.ndarray:

    if not (isinstance(data, np.ndarray)):
        raise ValueError("data must be a np.ndarray")


    indexes = np.argsort(data, kind=key, axis=0)
    data_sorted = np.sort(data, kind=key, axis=0)

    # abscissa
    X_ind = indexes[::, 0]
    X_sorted = data_sorted[::, 0]

    q1_X = int(X_sorted[int(len(X_sorted) * 0.25)])
    q3_X = int(X_sorted[int(len(X_sorted) * 0.75)])
    X_E = int(1.5 * (q3_X - q1_X))

    X_lower = X_sorted < q1_X - X_E
    X_upper = X_sorted > q3_X + X_E

    X_ind_slice = np.append(X_ind[X_lower], X_ind[X_upper])

    # ordinates
    Y_ind = indexes[::, 1]
    Y_sorted = data_sorted[::, 1]

    q1_Y = round(Y_sorted[int(len(Y_sorted) * 0.25)])
    q3_Y = round(Y_sorted[int(len(Y_sorted) * 0.75)])
    Y_E = int((q3_Y - q1_Y) * 1.5)

    Y_lower = Y_sorted < q1_Y - Y_E
    Y_upper = Y_sorted > q3_Y + Y_E

    Y_indexes_slice = np.append(
        Y_ind[Y_lower],
        Y_ind[Y_upper],
    )

    return X_ind_slice, Y_indexes_slice