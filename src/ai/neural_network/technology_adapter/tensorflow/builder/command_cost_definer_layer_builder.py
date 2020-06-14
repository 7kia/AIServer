from typing import Dict

from tensorflow.keras import layers

from src.ai.neural_network.technology.tensorflow.networks.network_adapter import InputParamCostDefinerLayerNames, \
    CommandCostDefinerLayerNames
from src.ai.neural_network.technology_adapter.builder.command_cost_definer_layer_builder import \
    CommandCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers, NetworkLayer
from src.ai.neural_network.technology_adapter.tensorflow.builder.tensorflow_layer_builder import TensorflowLayerBuilder
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class TensorflowCommandCostDefinerLayerBuilder(CommandCostDefinerLayerBuilder, TensorflowLayerBuilder):
    def __init__(self):
        super().__init__()

    def generate_for_unit_observation_layer(self, input_layers: NetworkLayers) -> Dict[str, NetworkLayer]:
        return self._generate_from(input_layers,
                                   InputParamCostDefinerLayerNames.unit_observation,
                                   CommandCostDefinerLayerNames.unit_observation)

    def generate_for_sector_params_layer(self, input_layers: NetworkLayers) -> Dict[str, NetworkLayer]:
        return self._generate_from(input_layers,
                                   InputParamCostDefinerLayerNames.sector_params,
                                   CommandCostDefinerLayerNames.sector_params)

    def generate_for_person_unit_params_layer(self, input_layers: NetworkLayers) -> Dict[str, NetworkLayer]:
        return self._generate_from(input_layers,
                                   InputParamCostDefinerLayerNames.person_unit_params,
                                   CommandCostDefinerLayerNames.person_unit_params)

    def _generate_from(self,
                       input_layers: NetworkLayers,
                       input_layer_key: str,
                       new_layer_name: str) -> Dict[str, TensorflowNetworkLayer]:
        result: Dict[str, TensorflowNetworkLayer] = {}
        current_layer: TensorflowNetworkLayer = input_layers[input_layer_key]
        size: int = len(current_layer.value.units)
        for tensor_name in command_cost_definer_tensor_names:
            result[tensor_name.value] = TensorflowNetworkLayer()
            result[tensor_name.value].value = layers.Dense(
                size,
                activation='relu',
                name=f"{new_layer_name}__{tensor_name}"
            )(
                self._convert_as_array(current_layer)
            )
        return result
