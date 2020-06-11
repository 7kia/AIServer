from typing import List

from src.ai.ai import Ai
from src.ai.ai_command_generator import Json
from src.ai.game_components.command_data_generation import CommandDataGeneration
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit import UnitList
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
import numpy as np

class NeuralNetwork(Ai):
    _network_adapter: NetworkAdapter = None

    def __init__(self):
        super().__init__()

    def get_commands(self, game_state: GameState) -> List[Json]:
        self.set_last_game_state(self._current_game_state)
        self.set_current_game_state(game_state)

        result: List[Json] = []
        # TODO 7kia дальше нужно выбрать конкретный тип подразделений в зависимости
        # от подтипа слоя

        units: UnitList = game_state.game_units.own_units["regiments"]
        for unit in units:
            unit_observation: UnitObservation = UnitObservation()
            unit_observation.set(game_state.sector_params, unit)
            command: Json = {}
            if self.is_train():
                command = self._network_adapter.train(
                    CommandDataGeneration(unit.id, unit.position),
                    unit_observation,
                    self.get_current_game_state(), self.get_last_game_state()
                )
            else:
                command = self._network_adapter.test(
                    CommandDataGeneration(unit.id, unit.position),
                    unit_observation,
                    self.get_current_game_state()
                )
            result += command
        return result

    def _generate_commands(self) -> List[Json]:
        return []

    def train(self, game_state: GameState) -> List[Json]:
        commands: List[Json] = self.get_commands(game_state)
        return commands

    def set_network_adapter(self, network_adapter: NetworkAdapter):
        self._network_adapter = network_adapter
