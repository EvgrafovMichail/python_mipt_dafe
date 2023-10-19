"""
В этом модуле хранятся утилиты для визуализации
"""


import contextlib

import matplotlib.pyplot as plt

from lsm_project.lsm.models import LSMLines


@contextlib.contextmanager
def switch_to_ggplot() -> None:
    """
    Контекстный менеджер для смены стиля на ggplot
    """

    plt.style.use('ggplot')

    try:
        yield

    finally:
        plt.style.use('default')


def visualize_lines(lines: LSMLines, path_to_save='lsm.png') -> None:
    """
    Функция для визуализации МНК и сохранения полученной картинки

    :param: lines - объект с описанием линий
    :param: path_to_save - путь для сохранения изображения
    """

    _, ax = plt.subplots(figsize=(16, 9))

    color_main, color_support = 'orangered', 'lightsalmon'

    ax.scatter(
        lines.abscissa, lines.ordinates, c=color_support,
        s=20, label='experiment data'
    )

    ax.plot(
        lines.abscissa, lines.line_predicted, c=color_main,
        label='predicted line'
    )
    ax.plot(
        lines.abscissa, lines.line_above, c=color_main,
        linestyle='--', label='error'
    )
    ax.plot(
        lines.abscissa, lines.line_under, c=color_main,
        linestyle='--'
    )

    ax.set_xlim(min(lines.abscissa), max(lines.abscissa))

    ax.legend()
    ax.grid(True)

    plt.savefig(path_to_save)
