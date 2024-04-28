from os.path import isfile
from warnings import warn
import matplotlib.pyplot as plt


def save_file(path_to_save: str) -> None:
    path_to_save += "/graphic.png"
    if isfile(path_to_save):
        warn("Image file graphic.png will be overwritten")
    plt.savefig(path_to_save, bbox_inches="tight")
