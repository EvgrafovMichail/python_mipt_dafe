import os
import warnings
from matplotlib import pyplot as plt


def visualize_results(
        axis: plt.Axes,
        abscissa: list,
        ordinates: list,
        predictions: list,
        abcissa_error: list=[],
        ordinates_error_lower: list=[],
        ordinates_error_upper: list=[],
        path_to_save: str=''
) -> None:
    if len(abcissa_error) != 0 and len(ordinates_error_lower) != 0 and len(ordinates_error_upper) != 0:
        axis.fill_between(abcissa_error, ordinates_error_lower, ordinates_error_upper,label='errors', color='red',linestyle='dashed', alpha=0.1)
    axis.scatter(abscissa, ordinates, label='source', c='royalblue', s=1)
    axis.plot(abscissa, predictions, label='prediction', c='steelblue')

    axis.set_xlim(min(abscissa), max(abscissa))
    axis.legend()
    if len(path_to_save) != 0:
        if os.path.isfile(path_to_save):
            warnings.warn("В указанном пути есть файл, мы его заменили")
        plt.savefig(path_to_save)