from src.unit import Unit
from src.unit_state_extractor import UnitStateExtractor

Json = dict


class UnitFactory:
    @staticmethod
    def create_unit(json: Json):
        unit = Unit()
        unit.id = int(json["id"])
        unit.unit_type = int(json["type"])
        unit.state = UnitStateExtractor.extract_state(json)

        return unit
