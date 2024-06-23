import os
import warnings
import matplotlib.pyplot as plt


def visualize_results(
    axis: plt.Axes,
    abscissa: list,
    ordinates: list,
    predictions: list,
    abcissa_error: list = [],
    ordinates_error_lower: list = [],
    ordinates_error_upper: list = [],
    path_to_save: str = ''
) -> None:
    if abcissa_error.any() and ordinates_error_lower.any() and ordinates_error_upper.any():
        axis.fill_between(
            abcissa_error, ordinates_error_lower, ordinates_error_upper,
            label='errors', color='red', linestyle='dashed', alpha=0.1
        )

    axis.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)
    axis.plot(abscissa, predictions, label='prediction', c='steelblue')

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()

    if path_to_save:
        if os.path.isfile(path_to_save):
            warnings.warn("File already exists at the specified path, overwriting it.")
        plt.savefig(path_to_save)
