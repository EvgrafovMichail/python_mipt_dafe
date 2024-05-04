from enum import Enum

DEFAULT_COLORS = ("royalblue", "darkorange")


class Metric(Enum):
    MANHATTAN = "l1"
    EUCLIDEAN = "l2"


class PlotType(Enum):
    VIOLIN = "violin"
    HIST = "hist"
    BOX = "boxplot"
