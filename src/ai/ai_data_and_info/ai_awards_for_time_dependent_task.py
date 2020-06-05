from src.ai.ai_data_and_info.ai_awards import AiAwards
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
