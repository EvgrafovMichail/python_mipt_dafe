from enum import Enum


class Diagram_types(Enum):
    VIOLIN = "violin"
    HIST = "hist"
    BOXPLOT = "boxplot"

Diagram_types = [
    "violin", 
    "hist", 
    "boxplot"
]

if "violin" in Diagram_types:
    print(10)