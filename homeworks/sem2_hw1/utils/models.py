from enum import Enum


class SortingKeys(Enum):
    QUICKSORT = 'quicksort'
    MERGESORT = 'mergesort'
    HEAPSORT = 'heapsort'
    STABLE = 'stable'


class Colors(Enum):
    RED = 'r'
    GREEN = 'g'
    BLUE = 'b'
    CYAN = 'c'
    MAGENTA = 'm'
    YELLOW = 'y'
    BLACK = 'k'


class DiagramType(Enum):
    VIOLIN = "violin"
    HIST = "hist"
    BOXPLOT = "boxplot"


class RegressionVisualizeSettings:
    def __init__(
        self,
        points_size=1,
        points_color='#5353ff',
        prediction_color='#ff3131',
        error_color='#735184',
        error_linestyle='--'
    ):
        self._points_size = points_size
        self._points_color = points_color
        self._prediction_color = prediction_color
        self.error_color = error_color
        self.error_linestyle = error_linestyle


class ComparisonSettings:
    def __init__(
        self,
        fontsize=15,
        fontweight="bold",
        title_color="dimgray",
        colors=list(Colors),
    ):
        self._fontsize = fontsize
        self._fontweight = fontweight
        self._title_color = title_color
        self._colors = colors


class OutliersSettings:
    _low_border: int
    _high_border: int
    _epsilon: int
    def __init__(
        self,
        low_border=0.25,
        high_border=0.75,
        epsilon=1.5
    ):
        self._low_border = low_border
        self._high_border = high_border
        self._epsilon = epsilon


class HistogramSettings:
    def __init__(
            self,
            bins=50,
            color="cornflowerblue",
            edgecolor=None,
            density=True,
            alpha=0.5,
            orientation="vertical"
            ):
        self._bins = bins
        self._color = color
        self._edgecolor = edgecolor
        self._density = density
        self._alpha = alpha
        self._orientation = orientation


class BoxplotSettings:
    def __init__(
            self,
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="lightsteelblue"),
            medianprops=dict(color="k"),
    ):
        self._vert = vert
        self._patch_artist = patch_artist
        self._boxprops = boxprops
        self._medianprops = medianprops


class ViolinSettings:
    def __init__(
        self,
        vert=False,
        showmedians=True,
        facecolor="cornflowerblue",
        edgecolor="blue",
        othercolor="cornflowerblue",
        orientation="vertical",
    ):
        self._vert = vert
        self._showmedians = showmedians
        self._facecolor = facecolor
        self._edgecolor = edgecolor
        self._othercolor = othercolor
        self._orienattion = orientation


class MegahistSettings:
    def __init__(
        self,
        settings=None,
        space=0.2,  # В таком порядке, т.к. их размерность должна в возрастающем порядке идти
        alpha=0.5,
        grid_ratio=(4, 4),
        color="cornflowerblue",
    ):
        self._space = space
        self._alpha = alpha
        self._grid_ratio = grid_ratio
        self._color = color
        self._settings = settings
