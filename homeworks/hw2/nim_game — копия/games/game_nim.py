from nim_game.environments.environment_nim import EnvironmentNim
from nim_game.common.models import NimStateChange, GameState
from nim_game.agents.agent import Agent
from nim_game.common.enumerations import Players

import json


class GameNim:
    _environment: EnvironmentNim  # состояния кучек
    _agent: Agent  # бот

    def __init__(self, path_to_config: str) -> None:

        with open(path_to_config) as file:
            file_read = json.load(file)
            self._agent = Agent(file_read["opponent_level"])
            self._environment = EnvironmentNim(file_read["heaps_amount"])

    def make_steps(self, player_step: NimStateChange) -> GameState:

        self._environment.change_state(player_step)

        if self.is_game_finished():
            winner = Players.USER
            return GameState(winner)

        opponent = self._agent.make_step(self._environment.get_state())

        opponent.heap_id += 1

        self._environment.change_state(opponent)

        if self.is_game_finished():
            winner = Players.BOT
            return GameState(winner)

        return GameState(None, opponent, self._environment.get_state())

    def is_game_finished(self) -> bool:
        if sum(self.heaps_state) == 0:
            return True
        return False

    @property
    def heaps_state(self) -> list[int]:
        return self._environment.get_state()
