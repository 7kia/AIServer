from typing import Dict

from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer, NetworkLayers
from src.ai.neural_network.technology_adapter.optimizer import Optimizer
from src.ai.neural_network.technology_adapter.tensorflow.scout_network_adapter import ScoutNetworkAdapter


class NetworkTechnologyAdapterBuilder:
    def __init__(self):
        pass

    @staticmethod
    def generate_scout_network_adapter(ai_info: AiInfo) -> ScoutNetworkAdapter:
        return ScoutNetworkAdapter()

    def generate_error_function(self, ai_awards_definer: AiAwardsDefiner) -> ErrorFunction:
        return ErrorFunction()

    def generate_optimizer(self) -> Optimizer:
        return Optimizer()

    def compile_model(self,
                      adapter: NetworkAdapter,
                      error_function: ErrorFunction, optimizer: Optimizer) -> NetworkAdapter:
        pass

    def generate_input_unit_observation_layer(self) -> NetworkLayers:
        pass

    def generate_input_sector_params_layer(self) -> NetworkLayers:
        pass

    def generate_input_person_unit_params_layer(self) -> NetworkLayers:
        pass

    def generate_command_definer_layer(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        pass

    def generate_output_layer(self, input_layer: NetworkLayer) -> NetworkLayers:
        pass







