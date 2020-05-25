from enum import Enum
from typing import Dict, List

from src.ai.game_components.game_state import GameState
from src.ai.game_components.game_units import GameUnits
from src.ai.game_components.person_unit_params import PersonUnitParams
from src.ai.game_components.sector_params import SectorParams
from src.ai.game_components.unit import UnitDict, Unit
from src.ai.game_components.unit_factory import UnitFactory

Json = Dict[str, any]


class UnitCategory(Enum):
    regiment: str = "regiment"
    base: str = "base"
    support: str = "support"


class GameDataExtractor:
    @classmethod
    def extract_game(cls, json_file_content: Json) -> GameState:
        game_state = GameState()
        game_state.game_units = cls._extract_game_unit(json_file_content)

        game_state.person_unit_params = cls._extract_person_unit_params(json_file_content)
        game_state.sector_params = cls._extract_sector_params(json_file_content)
        return game_state

    @classmethod
    def _extract_game_unit(cls, json_file_content: Json) -> GameUnits:
        unit_dictionary = json_file_content["units"]
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

    @classmethod
    def _extract_person_unit_params(cls, json_file_content: Json):
        person_unit_params = PersonUnitParams()
        person_unit_params.troopAmount = json_file_content["troopAmount"]
        person_unit_params.organization = json_file_content["organization"]
        person_unit_params.experience = json_file_content["experience"]
        person_unit_params.overlap = json_file_content["overlap"]
        return person_unit_params

    @classmethod
    def _extract_sector_params(cls, json_file_content: Json):
        sector_params = SectorParams()
        sector_params.ownUnitToSectors = cls._extract_units_from_sectors(json_file_content["ownUnitToSectors"])
        sector_params.enemyUnitToSectors = cls._extract_units_from_sectors(json_file_content["enemyUnitToSectors"])

        sector_params.ownSumInfo = json_file_content["ownSumInfo"]
        sector_params.ownMaxInfo = json_file_content["ownMaxInfo"]
        sector_params.enemySumInfo = json_file_content["enemySumInfo"]
        sector_params.enemyMaxInfo = json_file_content["enemyMaxInfo"]
        return sector_params

    @classmethod
    def _extract_units_from_sectors(cls, matrix: List[List[List[Json]]]) -> List[List[List[Unit]]]:
        result: List[List[List[Unit]]] = []
        for y in range(0, len(matrix)):
            result.append([])
            for x in range(0, len(matrix[y])):
                result.append([])
                unit_list: List[Json] = matrix[y][x]
                for unit_json in unit_list:
                    result[y][x].append(UnitFactory.create_unit(unit_json))
        return result
