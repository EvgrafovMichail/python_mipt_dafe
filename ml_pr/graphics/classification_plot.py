import numpy as np
import matplotlib.pyplot as plt
import os
import warnings


def classification_plot(
    points: np.ndarray, 
    lables: np.ndarray,
    path_to_save: str="", 
    colors = []
) -> None:
    
    figure = plt.figure(figsize=(8, 8))
    axis = figure.add_subplot()
    axis.set_title("classification", fontweight='bold')

    if len(colors) == 0:
        for label in np.unique(lables):
            axis.scatter(*points[lables == label].T, alpha=0.5)
    else:
        for i, label in enumerate(np.unique(lables)):
            color = colors[i % len(colors)]
            axis.scatter(*points[lables == label].T, color=color, alpha=0.5)

    if(len(path_to_save) != 0):
        if os.path.isfile(path_to_save):
            warnings.warn(
                "\nFile with same name already exist\n"
            )
        plt.savefig(path_to_save)

    plt.show()