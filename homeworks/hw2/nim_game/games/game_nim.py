import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent

from nim_game.common.enumerations import Players # Убрать мб потом

class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        with open(path_to_config, mode = 'r') as data:
            game_config_json = data.read()
        game_config = json.loads(game_config_json)

        self._environment = EnvironmentNim(game_config["heaps_amount"])
        self._agent = Agent(game_config["opponent_level"])



    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """
        heaps_state = self._environment.get_state()

        heaps_state[player_step.heap_id] -= player_step.decrease
        if self.is_game_finished():
            return GameState(winner = Players.USER)

        opponent_step = self._agent.make_step(heaps_state=heaps_state)
        heaps_state[opponent_step.heap_id] -= opponent_step.decrease   # Как же хочется подтирать за собой память
        if self.is_game_finished():
            return GameState(winner = Players.BOT)

        return GameState(opponent_step = opponent_step, heaps_state=heaps_state)

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        for heap in self._environment.get_state():
            if heap > 0:
                return False
        return True

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
