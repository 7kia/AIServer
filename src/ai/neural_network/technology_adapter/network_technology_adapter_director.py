from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
from src.ai.neural_network.technology_adapter.network_technology_adapter_builder import NetworkTechnologyAdapterBuilder
from src.ai.neural_network.technology_adapter.optimizer import Optimizer
from src.ai.neural_network.technology_adapter.tensorflow.scout_network_adapter import ScoutNetworkAdapter
from src.ai.neural_network.technology_adapter.tensorflow.tensorflow_network_adapter_builder import \
    TensorflowNetworkAdapterBuilder


class NetworkTechnologyAdapterDirector:
    def __init__(self):
        self._builder: NetworkTechnologyAdapterBuilder = TensorflowNetworkAdapterBuilder()
    
    def generate_scout_network_adapter(self,
                                       ai_info: AiInfo,
                                       ai_awards_definer: AiAwardsDefiner) -> NetworkAdapter:
        result: ScoutNetworkAdapter = self._builder.generate_scout_network_adapter(ai_info)
        result.set_layer_1(self._builder.generate_layer_1())

        error_function: ErrorFunction = self._builder.generate_error_function(ai_awards_definer)
        optimizer: Optimizer = self._builder.generate_optimizer()
        return self._builder.compile_model(result, error_function, optimizer)

