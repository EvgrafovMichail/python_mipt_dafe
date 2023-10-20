"""
В этом модуле хранится специальны класс для логирования
"""


import logging

from enum import Enum


# уровни логирования 
class Levels(Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR


class EventLogger:
    _logger: logging.Logger

    def __init__(self, level: Levels = Levels.debug) -> None:
        if not isinstance(level, Levels):
            raise ValueError(
                f'unexpected level type: {type(level).__name__}'
            )

        self._logger = logging.getLogger('event_logger')

        formatter = logging.Formatter(
            '[%(levelname)s]: || %(asctime)s || %(message)s;'
        )

        handler = logging.StreamHandler()
        handler.setLevel(level.value)
        handler.setFormatter(formatter)

        self._logger.setLevel(level.value)
        self._logger.addHandler(handler)

    def debug(self, message: str) -> None:
        """
        Функция для вывода отладочной информации
        """
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """
        Функция для вывода информации по ходу выполнения
        """
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """
        Функция для вывода информации о предупреждениях
        """
        self._logger.warning(message)

    def error(self, message: str) -> None:
        """
        Функция для вывода информации об ошибках
        """
        self._logger.error(message)
