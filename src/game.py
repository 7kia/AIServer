from typing import Dict

from src.unit import Unit, UnitList


class Game:
    def __init__(self):
        self.id: int = -1
        self.users: Dict[str, str] = {}
        self.unit_dictionary: Dict[str, UnitList] = {}

