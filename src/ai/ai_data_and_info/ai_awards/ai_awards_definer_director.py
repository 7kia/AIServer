from src.ai.ai import Ai
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_for_time_dependent_task import AiAwardsDefinerForTimeDependentTask
from src.ai.neural_network.scout_network import ScoutNetwork


class AiAwardsDefinerDirector:
    @staticmethod
    def create_for_ai(ai: Ai) -> AiAwardsDefiner:
        if type(ai) is ScoutNetwork:
            return AiAwardsDefinerForTimeDependentTask()
        return AiAwardsDefiner()
