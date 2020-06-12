from enum import Enum
from typing import List, Dict

from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.neural_network.technology_adapter.builder.command_cost_definer_layer_builder import \
    CommandCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.builder.input_param_cost_definer_layer_builder import \
    InputParamCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer, NetworkLayers
from src.ai.neural_network.technology_adapter.network_technology_adapter_builder import NetworkTechnologyAdapterBuilder
from src.ai.neural_network.technology_adapter.optimizer import Optimizer
from src.ai.neural_network.technology_adapter.tensorflow.builder.command_cost_definer_layer_builder import \
    TensorflowCommandCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.tensorflow.builder.input_param_cost_definer_layer_builder import \
    TensorflowInputParamCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.tensorflow.scout_network_adapter import ScoutNetworkAdapter
from src.ai.neural_network.technology_adapter.tensorflow.tensorflow_network_adapter_builder import \
    TensorflowNetworkAdapterBuilder


class InputLayerNames(Enum):
    unit_observation: str = "unit_observation"
    person_unit_params: str = "person_unit_params"
    sector_params: str = "sector_params"


class InputParamCostDefinerLayerNames(Enum):
    unit_observation: str = "unit_observation__cost_definer"
    person_unit_params: str = "person_unit_params__cost_definer"
    sector_params: str = "sector_params__cost_definer"


class CommandCostDefinerLayerNames(Enum):
    unit_observation: str = "unit_observation__command_cost_definer"
    person_unit_params: str = "person_unit_params__command_cost_definer"
    sector_params: str = "sector_params__command_cost_definer"


command_cost_definer_layer_names: List[CommandCostDefinerLayerNames] = []
for name in CommandCostDefinerLayerNames:
    command_cost_definer_layer_names.append(name)


class CommandCostDefinerTensorNames(Enum):
    up: str = "up_command_cost_definer"
    up_right: str = "up_right_command_cost_definer"
    right: str = "right_command_cost_definer"
    down_right: str = "down_right_command_cost_definer"
    down: str = "down_command_cost_definer"
    down_left: str = "down_left_command_cost_definer"
    left: str = "left_command_cost_definer"
    up_left: str = "up_left_command_cost_definer"


command_cost_definer_tensor_names: List[CommandCostDefinerTensorNames] = []
for name in CommandCostDefinerTensorNames:
    command_cost_definer_tensor_names.append(name)


class CommandCostDefinerTensorId(Enum):
    up: int = 0
    up_right: int = 1
    right: int = 2
    down_right: int = 3
    down: int = 4
    down_left: int = 5
    left: int = 6
    up_left: int = 7


class CommandDefinerLevel(Enum):
    command_cost_summation_layer: str = "command_cost_summation_layer"
    result: str = "result_layer"


class NetworkTechnologyAdapterDirector:
    def __init__(self):
        self._builder: NetworkTechnologyAdapterBuilder = TensorflowNetworkAdapterBuilder()
        self._input_param_cost_definer_builder: InputParamCostDefinerLayerBuilder \
            = TensorflowInputParamCostDefinerLayerBuilder()
        self._command_cost_definer_builder: CommandCostDefinerLayerBuilder \
            = TensorflowCommandCostDefinerLayerBuilder()

    def generate_scout_network_adapter(self,
                                       ai_info: AiInfo,
                                       ai_awards_definer: AiAwardsDefiner) -> NetworkAdapter:
        result: ScoutNetworkAdapter = self._builder.generate_scout_network_adapter(ai_info)

        input_layers: Dict[str, NetworkLayers] = self._build_input_layers()
        result.set_input_layers(input_layers)

        input_param_cost_definer: NetworkLayers = self._build_input_param_cost_definer_layers(input_layers)
        result.set_input_param_cost_definer(input_param_cost_definer)

        command_cost_definer_layer: Dict[str, NetworkLayers] = self._build_command_cost_definer_layers(
            input_param_cost_definer)
        result.set_command_cost_definer(command_cost_definer_layer)

        command_definer_layer: NetworkLayer = self._build_command_definer_layers(command_cost_definer_layer)
        result.set_command_definer(command_definer_layer)

        output_layer: NetworkLayers = self._build_output_layer(command_definer_layer)
        result.set_output_layer(output_layer)

        error_function: ErrorFunction = self._builder.generate_error_function(ai_awards_definer)
        optimizer: Optimizer = self._builder.generate_optimizer()
        return self._builder.compile_model(result, error_function, optimizer)

    def _build_input_layers(self) -> Dict[str, NetworkLayers]:
        result: Dict[str, NetworkLayers] = {
            InputLayerNames.unit_observation.__str__(): self._builder.generate_input_unit_observation_layer(),
            InputLayerNames.sector_params.__str__(): self._builder.generate_input_sector_params_layer(),
            InputLayerNames.person_unit_params.__str__(): self._builder.generate_input_person_unit_params_layer(),
        }
        return result

    def _build_input_param_cost_definer_layers(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayers:
        builder: InputParamCostDefinerLayerBuilder = self._input_param_cost_definer_builder
        result: NetworkLayers = {
            InputParamCostDefinerLayerNames.unit_observation.__str__():
                builder.generate_unit_observation_layer(
                    input_layers[InputLayerNames.unit_observation.__str__()]
                ),
            InputParamCostDefinerLayerNames.sector_params.__str__():
                builder.generate_sector_params_layer(
                    input_layers[InputLayerNames.sector_params.__str__()]
                ),
            InputParamCostDefinerLayerNames.person_unit_params.__str__():
                builder.generate_person_unit_params_layer(
                    input_layers[InputLayerNames.person_unit_params.__str__()]
                ),
        }
        return result

    def _build_command_cost_definer_layers(self, input_layers: NetworkLayers) -> Dict[str, NetworkLayers]:
        builder: CommandCostDefinerLayerBuilder = self._command_cost_definer_builder
        result: Dict[str, NetworkLayers] = {
            CommandCostDefinerLayerNames.unit_observation.__str__():
                builder.generate_for_unit_observation_layer(
                    input_layers
                ),
            CommandCostDefinerLayerNames.sector_params.__str__():
                builder.generate_for_sector_params_layer(
                    input_layers
                ),
            CommandCostDefinerLayerNames.person_unit_params.__str__():
                builder.generate_for_person_unit_params_layer(
                    input_layers
                ),
        }
        return result

    def _build_command_definer_layers(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        result: NetworkLayer = self._builder.generate_command_definer_layer(input_layers)
        return result

    def _build_output_layer(self, input_layer: NetworkLayer) -> NetworkLayers:
        result: NetworkLayers = self._builder.generate_output_layer(input_layer)
        return result
