import json

from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState, Players
from nim_game.agents.agent import Agent


class GameNim:
    _environment: EnvironmentNim        # состояния кучек
    _agent: Agent                       # бот

    def __init__(self, path_to_config: str) -> None:

        try:
            with open(path_to_config) as config:
                config = json.load(config)
                heaps_amount: int = config["heaps_amount"]
                opponent_level: str = config["opponent_level"]
        except:
            raise ValueError(
                "invalid path to config.json: "
                f"'{path_to_config}'"
            )

        self._environment = EnvironmentNim(heaps_amount)
        self._agent = Agent(opponent_level)

    def make_steps(self, player_step: NimStateChange) -> GameState:
        """
        Изменение среды ходом игрока + ход бота

        :param player_step: изменение состояния кучек игроком
        """
        self._environment.change_state(player_step)
        if self.is_game_finished():
            return GameState(Players.USER, player_step, self.heaps_state)

        bot_step = self._agent.make_step(self.heaps_state)

        self._environment.change_state(bot_step)
        if self.is_game_finished():
            return GameState(Players.BOT, bot_step, self.heaps_state)

        return GameState(None, bot_step, self.heaps_state)

    def is_game_finished(self) -> bool:
        """
        Проверить, завершилась ли игра, или нет

        :return: True - игра окончена, False - иначе
        """
        return not sum(self.heaps_state)

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
