import copy
from typing import List

from src.ai.ai import Ai
from src.ai.ai_command_generator import Json, CommandName, AiCommandGenerator
from src.ai.game_components.command_data_generation import CommandDataGeneration
from src.ai.game_components.game_state import GameState
from src.ai.game_components.position import Position
from src.ai.game_components.unit import UnitList
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
import numpy as np

SHOOTS_TO_SECOND: int = 25


class NeuralNetwork(Ai):
    _network_adapter: NetworkAdapter = None
    _troop_type: str = ""

    def __init__(self):
        super().__init__()

    def get_commands(self, game_state: GameState) -> List[Json]:
        if self._last_game_state is None:
            self.set_last_game_state(game_state)
            self.set_current_game_state(game_state)
        else:
            self.set_last_game_state(self._current_game_state)
            self.set_current_game_state(game_state)

        result: List[Json] = []
        units: UnitList = self._generate_access_unit_list(game_state)
        for unit in units:
            unit_observation: UnitObservation = UnitObservation()
            unit_observation.set(game_state.sector_params, unit)
            command: Json = {}
            if self.is_train():
                ai_command: AiCommand = self._network_adapter.train(
                    unit_observation,
                    self.get_current_game_state()
                )
                command = self._convert_to_json(
                    ai_command, CommandDataGeneration(unit.id, unit.position)
                )
            else:
                ai_command: AiCommand = self._network_adapter.test(
                    unit_observation,
                    self.get_current_game_state()
                )
                command = self._convert_to_json(
                    ai_command, CommandDataGeneration(unit.id, unit.position)
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

    def _generate_access_unit_list(self, game_state: GameState) -> UnitList:
        return game_state.game_units.own_units["regiments"]

    def set_troop_type(self, troop_type: str):
        self._troop_type = troop_type

    def _convert_to_json(self, command_numbers: AiCommand,
                         command_data: CommandDataGeneration) -> Json:
        choised_command: str = command_numbers.command_name
        new_position: Position = self._generate_new_position(
            command_data.position,
            command_numbers.direction.value,
            command_numbers.distance,
        )
        if choised_command == CommandName.stop_or_defence:
            return AiCommandGenerator.generate_stop_or_defence_command(
                command_data.id
            )
        elif choised_command == CommandName.retreat_or_storm:
            return AiCommandGenerator.generate_retreat_or_storm_command(
                command_data.id, new_position
            )
        elif choised_command == CommandName.move_or_attack:
            return AiCommandGenerator.generate_move_or_attack_command(
                command_data.id, new_position
            )
        raise IOError("_convert_to_json: not correct command")

    def _generate_new_position(self,
                               unit_position: Position,
                               direction: Position,
                               distance: float) -> Position:
        return self._generate_target_position(
            copy.copy(unit_position), direction, distance,
            self._location.bounds
        )
