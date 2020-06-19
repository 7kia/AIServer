import copy
from typing import List

from src.ai.ai_command_generator import Json, AiCommandGenerator, CommandName
from src.ai.game_components.command_data_generation import CommandDataGeneration
from src.ai.game_components.game_state import GameState
from src.ai.game_components.position import Position
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.optimizer import Optimizer


class NetworkAdapter:
    def __init__(self):
        pass

    def train(self,
              unit_observation: UnitObservation,
              current_game_state: GameState) -> AiCommand:
        pass

    def test(self,
             unit_observation: UnitObservation,
             current_game_state: GameState) -> AiCommand:
        pass

    def compile(self, optimizer: Optimizer, loss: ErrorFunction):
        pass
