import sys
from enum import Enum
from typing import Dict

from src.ai.game_components.unit_state import UnitState

Json = dict


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
