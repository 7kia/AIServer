from typing import List

from src.ai.ai_commands import Json
from src.ai.game_components.game_state import GameState
from src.ai.neural_network.neural_network import NeuralNetwork


class ScoutNetwork(NeuralNetwork):
    def __init__(self):
        super().__init__()

    def get_commands(self, game_state: GameState) -> List[Json]:
        return super().get_commands(game_state)

    def _generate_commands(self) -> List[Json]:
        return []
