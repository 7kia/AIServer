from typing import Dict

import numpy
from tensorflow import float32
import tensorflow as tf
from tensorflow.keras import layers

from src.ai.neural_network.technology.tensorflow.networks.network_adapter import InputParamCostDefinerLayerNames, \
    CommandCostDefinerLayerNames, command_cost_definer_tensor_names
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
                                   InputParamCostDefinerLayerNames.unit_observation.value,
                                   CommandCostDefinerLayerNames.unit_observation.value)

    def generate_for_sector_params_layer(self, input_layers: NetworkLayers) -> Dict[str, NetworkLayer]:
        return self._generate_from(input_layers,
                                   InputParamCostDefinerLayerNames.sector_params.value,
                                   CommandCostDefinerLayerNames.sector_params.value)

    def generate_for_person_unit_params_layer(self, input_layers: NetworkLayers) -> Dict[str, NetworkLayer]:
        return self._generate_from(input_layers,
                                   InputParamCostDefinerLayerNames.person_unit_params.value,
                                   CommandCostDefinerLayerNames.person_unit_params.value)

    def _generate_from(self,
                       input_layers: NetworkLayers,
                       input_layer_key: str,
                       new_layer_name: str) -> Dict[str, TensorflowNetworkLayer]:
        result: Dict[str, TensorflowNetworkLayer] = {}
        current_layer: TensorflowNetworkLayer = input_layers[input_layer_key]
        # size: int = len(current_layer.value.units)
        for tensor_name in command_cost_definer_tensor_names:
            result[tensor_name.value] = TensorflowNetworkLayer()
            result[tensor_name.value].value = layers.Dense(
                self._get_layer_size(current_layer),
                activation='relu',
                name=f"{new_layer_name}__{tensor_name.value}"
            )(
                current_layer.value
            )
        return result

    def _get_layer_size(self, layer: TensorflowNetworkLayer) -> int:
        type = layer.value.dtype
        if type.__eq__(float32):
            return tf.size(layer.value.shape[1])
        elif type.__eq__(numpy.float32):
            return tf.size(layer.value)
        raise TypeError(f"{layer.value.dtype} not use the network")
