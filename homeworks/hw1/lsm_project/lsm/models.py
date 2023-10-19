from dataclasses import dataclass


# структура данных для описания результатов МНК
@dataclass
class LSMDescription:
    incline: float                  # коэффициент наклона
    shift: float                    # смещение
    incline_error: float            # СКО коэффициента наклона
    shift_error: float              # СКО смещения


# структура данных для описания статистик МНК
@dataclass
class LSMStatistics:
    abscissa_mean: float            # среднее значение абсциссы
    ordinate_mean: float            # среднее значение ординаты
    product_mean: float             # среднее значение произведения
    abs_squared_mean: float         # среднее значения квадрата абсциссы


# структура данных для описания расчитанных линий
@dataclass
class LSMLines:
    abscissa: list[float]           # абсциссы
    ordinates: list[float]          # ординаты
    line_predicted: list[float]     # ординаты полученного решения
    line_above: list[float]         # ординаты верхней границы коридора ошибок
    line_under: list[float]         # ординаты нижней границы коридора ошибок
