from enum import Enum
from typing import Dict

from src.ai.game_components.game import Game
from src.ai.game_components.game_units import GameUnits
from src.ai.game_components.unit import UnitDict
from src.ai.game_components.unit_factory import UnitFactory

Json = Dict[str, any]


class UnitCategory(Enum):
    regiment: str = "regiment"
    base: str = "base"
    support: str = "support"


class GameDataExtractor:
    @staticmethod
    def extract_game(json_file_content: Json) -> Game:
        game = Game()
        game.id = json_file_content["id"]
        game.users = json_file_content["users"]
        game.game_units = GameDataExtractor._extract_game_unit(json_file_content["units"])
        return game

    @classmethod
    def _extract_game_unit(cls, unit_dictionary: Json) -> GameUnits:
        own_units: UnitDict = GameDataExtractor._extract_unit_dictionary(
            unit_dictionary["ownUnits"]
        )
        visible_enemy_units: UnitDict = GameDataExtractor._extract_unit_dictionary(
            unit_dictionary["visibleEnemyUnits"]
        )
        return GameUnits(own_units, visible_enemy_units)

    @staticmethod
    def _extract_unit_dictionary(json_content: Json) -> UnitDict:
        unit_dictionary: UnitDict = {}
        for unit_type in json_content.keys():
            unit_dictionary[unit_type] = []
            for unit_data in json_content[unit_type]:
                unit_dictionary[unit_type] \
                    .append(UnitFactory.create_unit(unit_data))
        return unit_dictionary
