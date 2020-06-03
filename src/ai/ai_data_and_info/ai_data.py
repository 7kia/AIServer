from typing import Dict

Json = Dict[str, any]


class AiData:
    def __init__(self, location: Json, country: str, game_state: Json):
        self.location: Json = location
        self.country: str = country
        self.game_state: Json = game_state
