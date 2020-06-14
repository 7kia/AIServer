import sys
from enum import Enum
from typing import Dict

from src.ai.game_components.convert_self_to_json import Json
from src.ai.game_components.unit_composition import UnitComposition
from src.ai.game_components.unit_state import UnitState


class UnitStatusFromJson(Enum):
    UNIT_STATUS_STOP: int = 1
    UNIT_STATUS_MARCH: int = 2
    UNIT_STATUS_ATTACK: int = 3
    UNIT_STATUS_DEFENCE: int = 4
    UNIT_STATUS_ATTACK_DEFENCE: int = 5
    UNIT_STATUS_RETREAT: int = 6


int_to_unit_states: Dict[int, UnitState] = {
    UnitStatusFromJson.UNIT_STATUS_STOP.value: UnitState(True, False, False),
    UnitStatusFromJson.UNIT_STATUS_MARCH.value: UnitState(False, False, False),
    UnitStatusFromJson.UNIT_STATUS_ATTACK.value: UnitState(True, True, False),
    UnitStatusFromJson.UNIT_STATUS_DEFENCE.value: UnitState(True, False, True),
    UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE.value: UnitState(True, True, True),
    UnitStatusFromJson.UNIT_STATUS_RETREAT.value: UnitState(False, True, False)
}

# 7kia Создан для того чтобы не тратить время на преобразование в число
string_to_int_presentation_unit_state: Dict[str, int] = {}
for enum_element in UnitStatusFromJson:
    string_to_int_presentation_unit_state[str(enum_element.value)] = enum_element


class UnitStateExtractor:
    @staticmethod
    def extract_state(json_content: Json) -> UnitState:
        # TODO 7kia возможно не работает(скрапкод)
        try:
            return int_to_unit_states[json_content["_status"]]
        except Exception as e:
            print("Unexpected error:", str(e))
            raise BaseException(f"Not the status {json_content['_status']}")

    @classmethod
    def extract_composition(cls, json_content: Json) -> UnitComposition:
        composition_json: Json = json_content["composition"]
        result: UnitComposition = UnitComposition()
        for key in composition_json.keys():
            current_element = composition_json[key]
            if isinstance(current_element, float):
                result.amount += current_element
            else:
                result.amount += current_element["quantity"]
                result.properties[key] = current_element
        return result
