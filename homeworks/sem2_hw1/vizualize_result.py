import numpy as np
import matplotlib.pyplot as plt
import os


def vizualize_classification(
    points: np.ndarray, 
    lables: np.ndarray,
    path_to_save: str, 
    colors = []
) -> None:
    figure = plt.figure(figsize=(8, 8))
    axis = figure.add_subplot()
    axis.set_title("classification", fontweight='bold')

    if len(colors) == 0:
        for label in np.unique(lables):
            axis.scatter(points[lables == label], alpha=0.5)
    else:
        for i, label in enumerate(np.unique(lables)):
            color = colors[i % len(colors)]
            axis.scatter(points[lables == label], color=color, alpha=0.5)

    if path_to_save != "":
        if os.path.exists(path_to_save + '.png'):
            print(f'Warning: the file {path_to_save} was overwritten')
        plt.savefig(path_to_save)


def vizualize_regression(
        abscissa: np.ndarray,
        ordinates: np.ndarray,
        predict: np.ndarray,
        path_to_save: str,
        down_error: np.ndarray = None,
        up_error: np.ndarray = None,
) -> None:
    figure = plt.figure(figsize=(8, 8))
    axis = figure.add_subplot()

    axis.set_title('NonparametricRegression')

    axis.scatter(abscissa, ordinates, label='source', c='cornflowerblue', s=1, alpha=0.5)
    axis.plot(
        abscissa, 
        predict,
        label='prediction',
        c='royalblue', 
        linewidth=1.5
    )
    
    if not down_error is None and not up_error is None:
        axis.plot(
            abscissa, 
            down_error,
            label='error',
            c='royalblue', 
            linewidth=1.5,
            linestyle='--'
        )
        axis.plot(
            abscissa, 
            up_error,
            c='royalblue', 
            linewidth=1.5,
            linestyle='--'
        )

    axis.legend()
    
    if path_to_save != "":
        if os.path.exists(path_to_save + '.png'):
            print(f'Warning: the file {path_to_save} was overwritten')
        plt.savefig(path_to_save)
