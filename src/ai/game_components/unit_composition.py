from typing import Dict

from src.ai.game_components.convert_self_to_json import Json


class UnitComposition:
    def __init__(self):
        self.properties: Dict[str, Json] = {}
        self.amount: float = 0
