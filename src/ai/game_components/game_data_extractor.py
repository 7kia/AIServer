from enum import Enum

from src.ai.game_components.game import Game
from src.ai.game_components.unit import Unit
from typing import Dict, List
from src.ai.game_components.unit_factory import UnitFactory

UnitList = List[Unit]
UnitDict = Dict[str, UnitList]
Json = dict


class UnitCategory(Enum):
    regiment: str = "regiment"
    base: str = "base"
    support: str = "support"


class GameDataExtractor:
    @staticmethod
    def extract_game(json_file_content: Dict[str, str]) -> Game:
        game = Game()
        game.id = json_file_content["id"]
        game.users = json_file_content["users"]
        game.unit_dictionary = json_file_content["units"]   # TODO 7kia convert to dict[str, Unit]
        return game

    @staticmethod
    def extract_unit_dictionary(json_content: Json) -> UnitDict:
        unit_dictionary: UnitDict = {}
        for unit_type in json_content.keys():
            unit_dictionary[unit_type] = []
            for unit_data in json_content[unit_type]:
                unit_dictionary[unit_type] \
                    .append(UnitFactory.create_unit(unit_data))
        return unit_dictionary
