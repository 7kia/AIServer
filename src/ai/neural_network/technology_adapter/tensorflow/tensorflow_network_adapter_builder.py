from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer
from src.ai.neural_network.technology_adapter.network_technology_adapter_builder import NetworkTechnologyAdapterBuilder
from src.ai.neural_network.technology_adapter.optimizer import Optimizer
from src.ai.neural_network.technology_adapter.tensorflow.tensorflow_error_function import TensorflowErrorFunction
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer
from src.ai.neural_network.technology_adapter.tensorflow.tensorflow_optimizer import TensorflowOptimizer
from src.ai.neural_network.technology_adapter.tensorflow.scout_network_adapter import ScoutNetworkAdapter


class TensorflowNetworkAdapterBuilder(NetworkTechnologyAdapterBuilder):
    def __init__(self):
        super().__init__()

    @staticmethod
    def generate_scout_network_adapter(ai_info: AiInfo) -> ScoutNetworkAdapter:
        return ScoutNetworkAdapter()

    def generate_layer_1(self) -> NetworkLayer:
        result: TensorflowNetworkLayer() = TensorflowNetworkLayer()
        return result

    def generate_error_function(self, ai_awards_definer: AiAwardsDefiner) -> ErrorFunction:
        return TensorflowErrorFunction(ai_awards_definer)

    def generate_optimizer(self) -> Optimizer:
        return TensorflowOptimizer()

    def compile_model(self,
                      adapter: NetworkAdapter,
                      error_function: ErrorFunction, optimizer: Optimizer) -> NetworkAdapter:
        # TODO 7kia обновить ErrorFunction и Optimizer
        adapter.compile(optimizer=optimizer, loss=error_function)
        return adapter
