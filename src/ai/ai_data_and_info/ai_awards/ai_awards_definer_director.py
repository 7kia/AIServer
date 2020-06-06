from src.ai.ai import Ai
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_builder import AiAwardsDefinerBuilder
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_for_time_dependent_task import AiAwardsDefinerForTimeDependentTask
from src.ai.neural_network.scout_network import ScoutNetwork


class AiAwardsDefinerDirector:
    def __init__(self):
        self.builder = AiAwardsDefinerBuilder()

    def create_for_ai(self, ai: Ai) -> AiAwardsDefiner:
        if type(ai) is ScoutNetwork:
            result: AiAwardsDefinerForTimeDependentTask = self.builder.create_for_time_dependent_task(ai)
            self.builder.set_ai_awards_properties(result)
            self.builder.set_time_dependent_properties(result)
            return result
        result: AiAwardsDefiner = self.builder.create(ai)
        self.builder.set_ai_awards_properties(result)
        return result
