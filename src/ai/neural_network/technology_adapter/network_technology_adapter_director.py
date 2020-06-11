from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer
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

        input_layer: NetworkLayer = self._builder.generate_input_layer()
        result.set_input_layer(input_layer)

        input_param_cost_definer: NetworkLayer = self._builder\
            .generate_input_param_cost_definer(input_layer)
        result.set_input_param_cost_definer(input_param_cost_definer)

        command_cost_definer_layer: NetworkLayer = self._builder\
            .generate_command_cost_definer(input_param_cost_definer)
        result.set_command_cost_definer(command_cost_definer_layer)

        output_layer: NetworkLayer = self._builder\
            .generate_output_layer(command_cost_definer_layer)
        result.set_output_layer(output_layer)

        error_function: ErrorFunction = self._builder.generate_error_function(ai_awards_definer)
        optimizer: Optimizer = self._builder.generate_optimizer()
        return self._builder.compile_model(result, error_function, optimizer)

