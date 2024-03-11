"""
Объекты для упрощения логирования
"""


import logging
import os

from enum import Enum


class Levels(Enum):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR


class EventLogger:
    _logger: logging.Logger

    def __init__(
        self,
        name: str,
        level: Levels = Levels.debug,
        path_to_logs: str = ''
    ) -> None:
        if not isinstance(level, Levels):
            raise ValueError(
                f'unexpected level type: {type(level).__name__}'
            )

        self._logger = logging.getLogger(name)

        formatter = logging.Formatter(
            '[%(levelname)s]: %(name)s || %(asctime)s || %(message)s;'
        )

        handler_console = logging.StreamHandler()
        handler_console.setLevel(level.value)
        handler_console.setFormatter(formatter)

        self._logger.setLevel(level.value)
        self._logger.addHandler(handler_console)

        if path_to_logs:
            path_to_folder = os.path.split(path_to_logs)[0]

            if path_to_folder and not os.path.exists(path_to_folder):
                os.makedirs(path_to_folder)

            handler_file = logging.FileHandler(path_to_logs)
            handler_file.setLevel(level.value)
            handler_file.setFormatter(formatter)

            self._logger.addHandler(handler_file)

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)
