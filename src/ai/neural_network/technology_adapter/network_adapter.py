from typing import List

from src.ai.ai_command_generator import Json, AiCommandGenerator, CommandName
from src.ai.game_components.command_data_generation import CommandDataGeneration
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.optimizer import Optimizer


class NetworkAdapter:
    def __init__(self):
        pass

    def train(self,
              command_data_generation: CommandDataGeneration,
              unit_observation: UnitObservation,
              current_game_state: GameState, last_game_state: GameState) -> Json:
        pass

    def test(self,
             command_data_generation: CommandDataGeneration,
             unit_observation: UnitObservation,
             current_game_state: GameState) -> Json:
        pass

    def compile(self, optimizer: Optimizer, loss: ErrorFunction):
        pass

    @staticmethod
    def _convert_to_json(command_numbers: AiCommand,
                         command_data: CommandDataGeneration) -> Json:
        choised_command: str = command_numbers.command_name.value
        if choised_command == CommandName.stop_or_defence:
            return AiCommandGenerator.generate_stop_or_defence_command(
                command_data.id
            )
        elif choised_command == CommandName.retreat_or_storm:
            return AiCommandGenerator.generate_retreat_or_storm_command(
                command_data.id, command_data.position
            )
        elif choised_command == CommandName.move_or_attack:
            return AiCommandGenerator.generate_move_or_attack_command(
                command_data.id, command_data.position
            )
        raise IOError("_convert_to_json: not correct command")
