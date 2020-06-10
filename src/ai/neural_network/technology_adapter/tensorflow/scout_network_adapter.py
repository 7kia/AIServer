from typing import List

from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology.tensorflow.networks.scout_network import ScoutNetwork
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
from src.ai.ai_commands import Json
from src.ai.neural_network.technology_adapter.optimizer import Optimizer


class ScoutNetworkAdapter(NetworkAdapter):
    def __init__(self):
        super().__init__()
        self._network: ScoutNetwork = ScoutNetwork()

    def train(self,
              unit_observation: UnitObservation,
              current_game_state: GameState,
              last_game_state: GameState) -> List[Json]:
        result: List[Json] = self._network.train(None, None)
        return result

    def test(self, unit_observation: UnitObservation,
             current_game_state: GameState) -> List[Json]:
        result: List[Json] = self._network.test(None, None)
        return result

    def compile(self, optimizer: Optimizer, loss: ErrorFunction):
        self._network.compile(optimizer, loss)

    def set_layer_1(self, param):
        pass
