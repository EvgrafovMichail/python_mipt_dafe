# функция для рассчета среднего значения величины
def mean(
        values: list[float],
) -> float:
    return sum(values) / len(values)


# функция для создания списка ординат (y), где y = kx + b
def line(
        incline: float, shift: float,
        abscissa: list[float],
) -> list[float]:
    return [incline*x + shift for x in abscissa]
