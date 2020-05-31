from typing import Dict

from src.ai.game_components.game_units import GameUnits
from src.ai.game_components.person_unit_params import PersonUnitParams
from src.ai.game_components.sector_params import SectorParams
from src.ai.game_components.unit import UnitDict


class GameState:
    def __init__(self):
        # self.id: int = -1
        # self.users: Dict[str, str] = {}
        self.game_units: GameUnits = GameUnits()
        self.person_unit_params: PersonUnitParams = PersonUnitParams()
        self.sector_params: SectorParams = SectorParams()

