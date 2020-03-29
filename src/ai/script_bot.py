import copy
from random import choice as random_choice
from typing import List

from src.ai.ai import Ai
from src.ai.ai_commands import AiCommands, Json, CommandName
from src.ai.game_components.game import Game
from src.ai.game_components.game_data_extractor import UnitDict
from src.ai.game_components.move_direction import DIRECTIONS, SHORT_DISTANCE, LONG_DISTANCE
from src.ai.game_components.position import Position
from src.ai.game_components.unit import UnitList, Unit


class ScriptBot(Ai):
    def __init__(self):
        super().__init__()

    def get_commands(self, game: Game) -> List[Json]:
        choised_unit: UnitList = self.choose_random_units(game.unit_dictionary)
        result: List[Json] = []
        for unit in choised_unit:
            result.append(self._generate_command_for_unit(unit, game))
        return result

    def _generate_command_for_unit(self, unit: Unit, game: Game) -> Json:
        access_commands: List[str] = self.generate_access_command_list(unit)
        choised_command: str = random_choice(access_commands)
        if choised_command == CommandName.stop_or_defence:
            return self._generate_stop_or_defence_command(unit, game)
        elif choised_command == CommandName.retreat_or_storm:
            return self._generate_retreat_or_storm_command(unit, game)
        elif choised_command == CommandName.move_or_attack:
            return self._generate_move_or_attack_command(unit, game)
        raise NotImplementedError("Incorrect command")

    @staticmethod
    def choose_random_units(unit_dictionary: UnitDict) -> UnitList:
        return Ai.choose_units(
            ScriptBot._get_random_units,
            unit_dictionary
        )

    def _generate_move_or_attack_command(self, unit: Unit, game: Game) -> Json:
        return AiCommands.generate_move_or_attack_command(unit.id, self._choice_random_position(unit.position))

    def _generate_retreat_or_storm_command(self, unit: Unit, game: Game) -> Json:
        return AiCommands.generate_retreat_or_storm_command(unit.id, self._choice_random_position(unit.position))

    def _generate_stop_or_defence_command(self, unit: Unit, game: Game) -> Json:
        return AiCommands.generate_stop_or_defence_command(unit.id)

    def _choice_random_position(self, unit_position: Position) -> Position:
        changed_direction: Position = random_choice(DIRECTIONS).value
        distance: float = self._change_distance()
        return self._generate_target_position(
            copy.copy(unit_position), changed_direction, distance,
            self._location.bounds
        )

    @staticmethod
    def _get_random_units(unit: Unit) -> bool:
        return random_choice([True, False])

    @staticmethod
    def _change_distance() -> float:
        return random_choice([SHORT_DISTANCE, LONG_DISTANCE])
