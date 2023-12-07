from random import choice, randint

from nim_game.common.enumerations import AgentLevels
from nim_game.common.models import NimStateChange


class Agent:
    """
    В этом классе реализованы стратегии игры для уровней сложности
    """

    _level: AgentLevels         # уровень сложности

    def __init__(self, level: str) -> None:
        pass

    def make_step(state_curr: list[int]) -> NimStateChange:
        """
        Сделать шаг, соотвутствующий уровню сложности

        :param state_curr: список целых чисел - состояние кучек
        :return: стуктуру NimStateChange - описание хода
        """
        pass
