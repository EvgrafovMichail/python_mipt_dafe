""" Реализация своего контекстного менеджера. 

    Пусть в начале работы файла задаётся точность вычислений с 
    плавающей точкой (например, 3 знака после запятой)

    И пусть где-то по ходу выполнения программы нам необходимо
    повысить точность вычислений (например, до 6-ти знаков после запятой)

    Как это можно сделать?
"""

from contextlib import contextmanager       # для создания собственного контекстного менеджера
                                            # можно использовать декоратор @contextmanager
from decimal import Decimal, getcontext


# пример регулировки точности вычислений
getcontext().prec = 3

result = Decimal('3') / Decimal('9') 
print(result)

print("current precise:", getcontext().prec)

getcontext().prec = 6

result = Decimal('3') / Decimal('9') 
print(result)

print("current precise:", getcontext().prec)
