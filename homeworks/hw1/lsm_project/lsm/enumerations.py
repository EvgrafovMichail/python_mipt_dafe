from enum import Enum


# перечисление с возможными стратегиями обработки
# несовпадения размеров списков
class MismatchStrategies(Enum):
    CUT = 'cut'                 # для обрезки длинного списка
    FALL = 'fall'               # для возбуждения исключения
