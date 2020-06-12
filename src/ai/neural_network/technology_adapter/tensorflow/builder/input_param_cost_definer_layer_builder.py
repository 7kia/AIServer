from typing import Dict, List

from tensorflow.keras import layers
from tensorflow.python.layers.base import Layer
import tensorflow as tf

from src.ai.neural_network.technology_adapter.builder.input_param_cost_definer_layer_builder import \
    InputParamCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers, NetworkLayer
from src.ai.neural_network.technology_adapter.network_technology_adapter_director import InputLayerNames, \
    InputParamCostDefinerLayerNames
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class TensorflowInputParamCostDefinerLayerBuilder(InputParamCostDefinerLayerBuilder):
    def __init__(self):
        super().__init__()

    def generate_unit_observation_layer(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        return self._generate_from(input_layers, InputLayerNames.unit_observation)

    def generate_sector_params_layer(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        return self._generate_from(input_layers, InputLayerNames.sector_params)

    def generate_person_unit_params_layer(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        return self._generate_from(input_layers, InputLayerNames.person_unit_params)

    def _generate_from(self,
                       input_layers: Dict[str, NetworkLayers],
                       concrete_layer_key: str) -> TensorflowNetworkLayer:
        result: TensorflowNetworkLayer = TensorflowNetworkLayer()
        current_layer: NetworkLayers = input_layers[concrete_layer_key]
        size: int = len(current_layer.keys())
        result.value = layers.Dense(
            size,
            activation='relu',
            name=InputParamCostDefinerLayerNames.unit_observation
        )(
            self._convert_as_array(current_layer)
        )
        return result

    def _convert_as_array(self, dictionary: NetworkLayers) -> tf.constant:
        array: List[Layer] = []
        for layer in dictionary.values():
            tensor: TensorflowNetworkLayer = layer
            array.append(tensor.value)
        return tf.constant(array)

    @staticmethod
    def _generate_size(input_tensor: TensorflowNetworkLayer):
        return len(input_tensor.value.keys())


