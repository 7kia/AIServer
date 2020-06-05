from src.ai.game_components.convert_self_to_json import ConvertSelfToJson, Json


class AiAwards(ConvertSelfToJson):
    def __init__(self):
        self.troop_amount: float = 0
        self.organization: float = 0
        self.experience: float = 0
        self.overlap: float = 0

    def as_json(self) -> Json:
        return {
            "troop_amount": self.troop_amount,
            "organization": self.organization,
            "experience": self.experience,
            "overlap": self.overlap,
        }

    def __iadd__(self, other):
        self.troop_amount += other.troop_amount
        self.organization += other.organization
        self.experience += other.experience
        self.overlap += other.overlap
        return self

    def clone_empty(self):
        return self.__init__()
