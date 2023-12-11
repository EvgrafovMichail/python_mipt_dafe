import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent

from nim_game.common.enumerations import Players # Убрать мб потом

class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config, mode = 'r') as data:  # Открытие и чтение файла
            game_config_json = data.read()
        game_config = json.loads(game_config_json)

        self._environment = EnvironmentNim(game_config["heaps_amount"])
        self._agent = Agent(game_config["opponent_level"])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота
        :param player_step: изменение состояния кучек игроком
        """
        player_step.heap_id -= 1   # Игрок не считает 0 натуральным числом
        # ход игрока
        self._environment.change_state(player_step)
        if self.is_game_finished():
            return GameState(winner = Players.USER)
        #ход бота
        opponent_step = self._agent.make_step(state_curr=self._environment.get_state())
        self._environment.change_state(opponent_step)
        if self.is_game_finished():
            return GameState(winner = Players.BOT)
        # игра продолжается
        return GameState(opponent_step = opponent_step, heaps_state=self._environment.get_state())

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет
        :return: True - игра окончена, False - иначе
        """
        return all([0 if i > 0 else 1 for i in self._environment.get_state()])

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
