from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction


class TensorflowErrorFunction(ErrorFunction):
    def __init__(self, ai_awards_definer: AiAwardsDefiner):
        super().__init__()

