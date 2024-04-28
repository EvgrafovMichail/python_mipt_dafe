import typing
from typing import Any
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import os
import warnings
from preprocessing.get_boxplot_outliers import get_boxplot_outliers

class TypeGraph:
    VIOLIN = violin = "VIOLIN"
    HIST = hist = "HIST"
    BOXPLOT = boxplot = "BOXPLOT"

def visualize_distribution(
    axis: plt.Axes,
    data: np.ndarray,
    diagram_type: Any,
    path_to_save: str = "",
) -> None:

    _supported_graphics = [TypeGraph.BOXPLOT, TypeGraph.VIOLIN, TypeGraph.HIST]

    diagram_type = str(diagram_type).upper()
    if(diagram_type not in _supported_graphics):
        raise ValueError("Please, change type of graphic")


    if(len(data.shape) == 1):
        if(diagram_type == "VIOLIN"):
            plt.violinplot(data)
        if(diagram_type == "BOXPLOT"):
            plt.boxplot(data)
        if(diagram_type == "HIST"):
            plt.hist(data)
        #plt.show()

    elif(len(data.shape) == 2 and data.shape[1] == 2):
        abscissa = data[0]
        ordinates = data[1]
        space = 0.2
        figure = plt.figure(figsize=(8, 8))
        grid = plt.GridSpec(4, 4, wspace=space, hspace=space)

        axis_scatter = figure.add_subplot(grid[:-1, 1:])
        axis_vert = figure.add_subplot(
            grid[:-1, 0],
            sharey=axis_scatter,
        )
        axis_hor = figure.add_subplot(
            grid[-1, 1:],
            sharex=axis_scatter,
        )

        axis_scatter.scatter(abscissa, ordinates, color="cornflowerblue", alpha=0.5)

        if(diagram_type == "HIST"):
            axis_hor.hist(
                abscissa,
                bins=50,
                color="cornflowerblue",
                density=True,
                alpha=0.5,
            )
            axis_vert.hist(
                ordinates,
                bins=50,
                color="cornflowerblue",
                orientation="horizontal",
                density=True,
                alpha=0.5,
            )

        if(diagram_type == "VIOLIN"):
            axis_hor.violinplot(
                abscissa,
                vert=False
            )
            axis_vert.violinplot(
                ordinates,
                vert=True
            )

        if(diagram_type == "BOXPLOT"):
            axis_hor.boxplot(
                abscissa,
                vert=False
            )
            axis_vert.boxplot(
                ordinates
            )

        axis_hor.invert_yaxis()
        axis_vert.invert_xaxis()

        #plt.show()
    else:
        raise TypeError("must be only 1 or 2 dimensions")
    

    if(len(path_to_save) != 0):
        if os.path.isfile(path_to_save):
            warnings.warn(
                "\nFile with same name already exist\n"
            )
        plt.savefig(path_to_save)

    plt.show()

