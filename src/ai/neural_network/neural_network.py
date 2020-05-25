from typing import List

from src.ai.ai import Ai
from src.ai.ai_commands import Json
from src.ai.game_components.game_state import GameState


class NeuralNetwork(Ai):
    def __init__(self):
        super().__init__()

    def get_commands(self, game_state: GameState) -> List[Json]:
        self.set_last_game_state(self._current_game_state)
        self.set_current_game_state(game_state)
        return self._generate_commands()

    def _generate_commands(self) -> List[Json]:
        return []
