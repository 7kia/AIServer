from typing import Dict, List

from tensorflow.keras import layers
from tensorflow.python.layers.base import Layer
import tensorflow as tf

from src.ai.neural_network.technology.tensorflow.networks.network_adapter import InputLayerNames, \
    InputParamCostDefinerLayerNames
from src.ai.neural_network.technology_adapter.builder.input_param_cost_definer_layer_builder import \
    InputParamCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers, NetworkLayer
from src.ai.neural_network.technology_adapter.tensorflow.builder.tensorflow_layer_builder import TensorflowLayerBuilder
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class TensorflowInputParamCostDefinerLayerBuilder(InputParamCostDefinerLayerBuilder, TensorflowLayerBuilder):
    def __init__(self):
        super().__init__()

    def generate_unit_observation_layer(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        return self._generate_from(input_layers,
                                   InputLayerNames.unit_observation,
                                   InputParamCostDefinerLayerNames.unit_observation)

    def generate_sector_params_layer(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        return self._generate_from(input_layers,
                                   InputLayerNames.sector_params,
                                   InputParamCostDefinerLayerNames.sector_params)

    def generate_person_unit_params_layer(self, input_layers: Dict[str, NetworkLayers]) -> NetworkLayer:
        return self._generate_from(input_layers,
                                   InputLayerNames.person_unit_params,
                                   InputParamCostDefinerLayerNames.person_unit_params)

    def _generate_from(self,
                       input_layers: Dict[str, NetworkLayers],
                       input_layer_key: str,
                       new_layer_name: str) -> TensorflowNetworkLayer:
        result: TensorflowNetworkLayer = TensorflowNetworkLayer()
        current_layer: NetworkLayers = input_layers[input_layer_key]
        size: int = len(current_layer.keys())
        result.value = layers.Dense(
            size,
            activation='relu',
            name=new_layer_name
        )(
            self._convert_as_array(current_layer)
        )
        return result

    @staticmethod
    def _generate_size(input_tensor: TensorflowNetworkLayer):
        return len(input_tensor.value.keys())


