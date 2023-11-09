""" управляемый map """

from enum import Enum
from itertools import zip_longest


class MapTypes(Enum):
    SHORTEST = 'short'
    LONGEST = 'long'

# Напишите функцию my_map() с дополнительными именованными аргументами 'type' и 'fill_value'.
# Если 'type' равен MapTypes.SHORTEST, то my_map должен работать как и встроенный map, обрезая
# все пришедшие коллекции по длине самой короткой коллекции.
# Если 'type' равен MapTypes.LONGEST, то все коллекции расширяются до длины самой длинной
# коллекции, а недостающие значения заоплняются значением 'fill_value'.
