from typing import Dict


class Game:
    def __init__(self):
        self.id: int = -1
        self.users: Dict[str, str] = {}
        self.unit_dictionary: Dict[str, str] = {}

