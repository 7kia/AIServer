from enum import Enum
from src.unit import Unit
from typing import Dict, List
from src.unit_factory import UnitFactory
from src.unit_state import UnitState

UnitList = List[Unit]
UnitDict = Dict[str, UnitList]
Json = dict


class UnitCategory(Enum):
    regiment: str = "regiment"
    base: str = "base"
    support: str = "support"


class GameDataExtractor:
    @staticmethod
    def extract_unit_dictionary(json_content: Json) -> UnitDict:
        unit_dictionary: UnitDict = {}
        for unit_type in json_content.keys():
            unit_dictionary[unit_type] = []
            for unit_data in json_content[unit_type]:
                unit_dictionary[unit_type] \
                    .append(UnitFactory.create_unit(unit_data))
        return unit_dictionary
