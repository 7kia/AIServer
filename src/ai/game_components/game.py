from typing import Dict

from src.ai.game_components.game_units import GameUnits
from src.ai.game_components.unit import UnitDict


class Game:
    def __init__(self):
        self.id: int = -1
        self.users: Dict[str, str] = {}
        self.game_units: GameUnits = None

