import typing
from typing import Any, Callable
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import warnings
import os
# ваш код


def make_coords(abscissa, ordinates):
    size_of_sample = abscissa.shape[0]
     #mnk coeff
    mnk = np.linalg.lstsq(np.vstack([abscissa, np.ones(len(abscissa))]).T, ordinates, rcond=None)[0] 

    #sigma coeff 

    sigma_y  = ((1 / (size_of_sample - 2)) * np.sum((ordinates - mnk[0] * abscissa - mnk[1]) ** 2))

    sigma_a = ((sigma_y ** 2) / (size_of_sample * ((abscissa ** 2).mean() - (abscissa.mean()) ** 2))) ** 0.5

    sigma_b = ((sigma_y ** 2 * (abscissa ** 2).mean()) / (size_of_sample * ((abscissa ** 2).mean() - (abscissa.mean()) ** 2))) ** 0.5


    x_mnk = mnk[0] * abscissa + mnk[1]

    y1 = (mnk[0] + sigma_a) * abscissa + mnk[1] + sigma_b
    y2 = (mnk[0] - sigma_a) * abscissa + mnk[1] - sigma_b


    return [x_mnk, y1, y2, mnk, abscissa, ordinates]




def mnk_show(x_mnk, y1, y2, mnk, abscissa, ordinates, borders):
    
    figure, axis = plt.subplots(figsize=(16, 9))

    axis.set_title(f"f(x) = {round(mnk[0], 2)}x + {round(mnk[1], 2)}", fontsize=17, fontweight="bold", c="dimgray")

    axis.scatter(
        abscissa,
        ordinates,
        color="royalblue",
        alpha = 0.8,
        label = "input data"
    );

    axis.plot(abscissa, x_mnk, color = "red", label = "approximation", linewidth=5);
    if(borders):
        axis.plot(abscissa, y1, color = "red", linestyle = '-.', label = "q - coridor");
        axis.plot(abscissa, y2, color = "red", linestyle = '-.');
        axis.fill_between(abscissa, y1, y2, color='g', alpha=0.2)

    axis.set_title('NonparametricRegression')
    axis.set_xlim(abscissa.min(), abscissa.max())
    axis.legend();
    


def regression_plot(
        data: np.ndarray,
        borders: bool = False,
        path_to_save: str = ""
    ):
    x = data[0]
    y = data[1]
    
    mnk_show(*make_coords(x, y), borders = borders)

    if(len(path_to_save) != 0):
        if os.path.isfile(path_to_save):
            warnings.warn(
                "\nFile with same name already exist\n"
            )
        plt.savefig(path_to_save)

    plt.show()
