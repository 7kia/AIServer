from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.game_components.convert_self_to_json import Json


class AiAwardsForTimeDependentTask(AiAwards):
    def __init__(self):
        super().__init__()
        self.speed: float = 0
        self.spent_time: float = 0

    def as_json(self) -> Json:
        result: Json = super().as_json()
        result["speed"] = self.speed
        result["spent_time"] = self.spent_time
        return result

    def __iadd__(self, other):
        super().__iadd__(other)
        self.speed += other.speed
        self.spent_time += other.spent_time
        return self

    def clone_empty(self):
        return AiAwardsForTimeDependentTask()

    def clone(self):
        copy = AiAwardsForTimeDependentTask()
        copy.troop_amount = self.troop_amount
        copy.organization = self.organization
        copy.experience = self.experience
        copy.overlap = self.overlap

        copy.speed = self.speed
        copy.spent_time = self.spent_time
        return copy

    def get_sum_award(self) -> float:
        return super().get_sum_award() + self.speed + self.spent_time
