from enum import Enum


class Metric(Enum):
    MANHATTAN = "l1"
    EUCLIDEAN = "l2"


class Plot_Type(Enum):
    LINE = "line"
    VIOLIN = "violin"
    HIST = "hist"
    BOX = "boxplot"
