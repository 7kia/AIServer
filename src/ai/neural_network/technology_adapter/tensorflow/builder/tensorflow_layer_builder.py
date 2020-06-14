from typing import List

from tensorflow.python.layers.base import Layer

from src.ai.neural_network.technology_adapter.builder.input_param_cost_definer_layer_builder import \
    InputParamCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers
import tensorflow as tf

from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class TensorflowLayerBuilder:
    def _convert_as_array(self, dictionary: NetworkLayers) -> tf.constant:
        array: List[Layer] = []
        for layer in dictionary.values():
            tensor: TensorflowNetworkLayer = layer
            array.append(tensor.value)
        return tf.constant(array)
