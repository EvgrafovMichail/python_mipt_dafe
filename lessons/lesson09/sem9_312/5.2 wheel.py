""" Реализация спиннера. 

    Интересная статья на тему индикаторов: https://dtf.ru/flood/174240-progress-bar-ili-spinner-chto-i-kogda-ispolzovat?ysclid=lorrg51syv550654720
    Возможно, вам поможет circle_generator...
"""
from typing import Iterable
from time import sleep, time

def wheel(time_limit: float, pause: float):
    """ Отрисовка спиннера.

        Печатает на экран надпись: 'Thinking: <symbol>',
        где вместо <symbol> последовательно появляются знаки: \, |, /, -, 
        что создаёт эффект вращения.

        Вход:
            time_limit: float
                время (в секундах), в течение которого должна производиться отрисовка спиннера
            pause: float
                время (в секундах) задержки между сменой символов спиннера
        
        Выход:
            None
    """
    pass