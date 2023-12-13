import json

from nim_game.common.models import NimStateChange, GameState, Players
from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.agents.agent import Agent


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:
        # if not path_to_config:
        #     raise ValueError("no path to file")
        with open(path_to_config) as f:
            json_file = json.load(f)

            self._environment = EnvironmentNim(json_file["heaps_amount"])
            self._agent = Agent(json_file["opponent_level"])

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """

        self._environment.change_state(player_step)
        if self.is_game_finished():
            return GameState(winner=Players.USER)

        bot_step = self._agent.make_step(self.heaps_state)
        bot_step.heap_id += 1
        self._environment.change_state(bot_step)
        if self.is_game_finished():
            return GameState(winner=Players.BOT)

        return GameState(
                opponent_step=bot_step,
                heaps_state=self.heaps_state
            )

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        return sum(self.heaps_state) == 0

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
