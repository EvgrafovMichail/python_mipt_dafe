from typing import Sequence, Optional
from numbers import Real

import matplotlib.pyplot as plt
import numpy as np


def visualize_1d_array(
    *,
    ordinate: Sequence[Real],
    abscissa: Optional[Sequence[Real]] = None,
    save_path: str = ""
) -> None:
    if ordinate is None:
        return

    with plt.style.context("ggplot"):
        figure, axis = plt.subplots(figsize=(16, 9))

        if abscissa is None:
            abscissa = np.arange(len(ordinate))

        else:
            abscissa = np.array(abscissa)

        axis.plot(abscissa, ordinate, c="royalblue")

        axis.set_xlim(abscissa.min(), abscissa.max())
        axis.grid(True)
        plt.show()

        if save_path:
            figure.savefig(save_path)
