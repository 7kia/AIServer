from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer
from src.ai.neural_network.technology_adapter.optimizer import Optimizer
from src.ai.neural_network.technology_adapter.scout_network_adapter import ScoutNetworkAdapter


class NetworkTechnologyAdapterBuilder:
    def __init__(self):
        pass

    @staticmethod
    def generate_scout_network_adapter(ai_info: AiInfo) -> ScoutNetworkAdapter:
        return ScoutNetworkAdapter()

    def generate_layer_1(self) -> NetworkLayer:
        return NetworkLayer()

    def generate_error_function(self) -> ErrorFunction:
        return ErrorFunction()

    def generate_optimizer(self) -> Optimizer:
        return Optimizer()

    def compile_model(self, error_function, optimizer):
        pass





