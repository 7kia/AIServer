from enum import Enum
from typing import List

from src.ai.game_components.unit_state import UnitState


class BaseType(Enum):
    land_base: str = "landbase"


class RegimentType(Enum):
    militia: str = "militia"
    motorized: str = "motorized"
    airborne: str = "airborne"
    marines: str = "marines"
    special: str = "special"
    engineer: str = "engineer"
    police: str = "police"
    tank: str = "tank"
    mechanized: str = "mechanized"
    artillery: str = "artillery"
    SPA: str = "SPA"
    costal_art: str = "costal_art"
    convoy: str = "convoy"
    train: str = "train"


class SupportType(Enum):
    truck: str = "truck"


class UnitType(Enum):
    bases: List[str] = [BaseType.land_base]
    regiments: List[str] = [
        RegimentType.militia, RegimentType.motorized,
        RegimentType.airborne, RegimentType.marines,
        RegimentType.special, RegimentType.engineer,
        RegimentType.police, RegimentType.tank,
        RegimentType.mechanized, RegimentType.artillery,
        RegimentType.SPA, RegimentType.costal_art,
        RegimentType.convoy, RegimentType.train
    ]
    supports: List[str] = [SupportType.truck]


class Unit:
    id: int = None
    unit_type: str = None
    state: UnitState = None

    def set(self, unit_id: int, unit_type: str, state: UnitState = UnitState()):
        self.id = unit_id
        self.unit_type = unit_type
        self.state = state
        return self


UnitList = List[Unit]
