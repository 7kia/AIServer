from typing import Dict

from src.ai.game_components.unit_factory import Json


class UnitComposition:
    def __init__(self):
        self.properties: Dict[str, Json] = {}
        self.amount: float = 0
