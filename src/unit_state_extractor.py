from enum import Enum
from src.unit_state import UnitState

Json = dict


class UnitStatusFromJson(Enum):
    UNIT_STATUS_STOP: int = 1
    UNIT_STATUS_MARCH: int = 2
    UNIT_STATUS_ATTACK: int = 3
    UNIT_STATUS_DEFENCE: int = 4
    UNIT_STATUS_ATTACK_DEFENCE: int = 5
    UNIT_STATUS_RETREAT: int = 6


unit_states = {
    UnitStatusFromJson.UNIT_STATUS_STOP: UnitState(True, False, False),
    UnitStatusFromJson.UNIT_STATUS_MARCH: UnitState(False, False, False),
    UnitStatusFromJson.UNIT_STATUS_ATTACK: UnitState(True, True, False),
    UnitStatusFromJson.UNIT_STATUS_DEFENCE: UnitState(True, False, True),
    UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE: UnitState(True, True, True),
    UnitStatusFromJson.UNIT_STATUS_RETREAT: UnitState(False, True, False)
}


class UnitStateExtractor:
    @staticmethod
    def extract_state(json_content: Json) -> UnitState:
        # TODO 7kia возможно не работает(скрапкод)
        return unit_states[int(json_content["_status"])]
