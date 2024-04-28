from typing import Optional, Any
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np

from utils.models import (
    DiagramType,
    ComparisonSettings,
    HistogramSettings,
    BoxplotSettings,
    ViolinSettings,
    MegahistSettings
)
from utils.plot_diagram import (
    plot_hist,
    plot_boxplot,
    plot_violin,
    plot_megahist,
)
from utils.save_file import save_file


FIGSIZE = (16, 9)


def visualize_scatter(
    points: np.ndarray,
    labels: np.ndarray,
    axis: Optional[plt.Axes] = None,
    settings: Optional[ComparisonSettings] = ComparisonSettings(),
) -> None:
    colors_cycle = cycle([color.value for color in settings._colors])
    labels_unique = np.unique(labels)

    if axis is None:
        _, axis = plt.subplots(figsize=FIGSIZE)

    for label in labels_unique:
        label_mask = labels == label
        axis.scatter(*points[label_mask].T, color=next(colors_cycle))

    axis.grid(True)


def visualize_comparison(
    points: np.ndarray,
    prediction: np.ndarray,
    expectation: np.ndarray,
    settings: Optional[ComparisonSettings] = ComparisonSettings(),
    path_to_save: Optional[str] = None,
) -> None:
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGSIZE)

    ax1.set_title("prediction",
                  fontsize=settings._fontsize,
                  fontweight=settings._fontweight,
                  c=settings._title_color)
    ax2.set_title("expectation",
                  fontsize=settings._fontsize,
                  fontweight=settings._fontweight,
                  c=settings._title_color)

    visualize_scatter(points, prediction, axis=ax1, settings=settings)
    visualize_scatter(points, expectation, axis=ax2, settings=settings)

    plt.show()

    if path_to_save:
        save_file(path_to_save)


def visualize_distribution(
    axis: list[plt.Axes],
    data: np.ndarray,
    diagram_type: Any,
    settings: Optional[MegahistSettings] = None,
    path_to_save: Optional[str] = None,
) -> None:
    # Подразумевается, что в одномерном случае axis подаются одни, а в двумерном - три
    if data.ndim == 1:
        match DiagramType(diagram_type):
            case DiagramType.HIST:
                plot_hist(axis=axis, data=data, settings=settings)
            case DiagramType.BOXPLOT:
                plot_boxplot(axis=axis, data=data, settings=settings)
            case DiagramType.VIOLIN:
                plot_violin(axis=axis, data=data, settings=settings)

    elif (data.ndim) == 2 and (data.shape[-1] == 2):
        if settings is None:
            match DiagramType(diagram_type):
                case DiagramType.HIST:
                    settings = MegahistSettings(settings=HistogramSettings)
                case DiagramType.BOXPLOT:
                    settings = MegahistSettings(settings=BoxplotSettings())
                case DiagramType.VIOLIN:
                    settings = MegahistSettings(settings=ViolinSettings())
                case _:
                    raise ValueError("Invalid diagram type")
        plot_megahist(axis=axis, data=data, diagram_type=diagram_type, settings=settings)

    else:
        raise ValueError("Data has invalid amount of dimensions")

    if path_to_save:
        save_file(path_to_save)
