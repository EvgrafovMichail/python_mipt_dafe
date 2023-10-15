from dataclasses import dataclass


@dataclass
class LSMDescription:
    incline: float
    shift: float
    incline_error: float
    shift_error: float


@dataclass
class LSMStatistics:
    abscissa_mean: float
    ordinate_mean: float
    product_mean: float
    abs_squared_mean: float


@dataclass
class LSMLines:
    abscissa: list[float]
    ordinates: list[float]
    line_predicted: list[float]
    line_above: list[float]
    line_under: list[float]
