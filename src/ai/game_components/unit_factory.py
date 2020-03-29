from typing import Dict

from src.ai.game_components.unit import Unit
from src.ai.game_components.unit_state_extractor import UnitStateExtractor

Json = Dict[str, any]


class UnitFactory:
    @staticmethod
    def create_unit(json: Json):
        unit = Unit()
        unit.id = int(json["id"])
        unit.unit_type = int(json["type"])
        unit.state = UnitStateExtractor.extract_state(json)

        return unit
