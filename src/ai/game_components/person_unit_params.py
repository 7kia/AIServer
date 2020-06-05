from src.ai.game_components.convert_self_to_json import ConvertSelfToJson, Json


class PersonUnitParams(ConvertSelfToJson):
    def __init__(self):
        self.troopAmount: float = 0
        self.organization: float = 0
        self.experience: float = 0
        self.overlap: float = 0
        self.speed: float = 0

    def as_json(self) -> Json:
        return {
            "troopAmount": self.troopAmount,
            "organization": self.organization,
            "experience": self.experience,
            "overlap": self.overlap,
            "speed": self.speed,
        }
