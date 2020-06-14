from typing import List, Dict

from tensorflow.python.keras import Input
from tensorflow.python.layers.base import Layer
from tensorflow.python.layers.core import Dense

from src.ai.neural_network.technology_adapter.builder.input_param_cost_definer_layer_builder import \
    InputParamCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers
import tensorflow as tf

from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class TensorflowLayerBuilder:
    @classmethod
    def convert_as_array(cls, dictionary: NetworkLayers) -> Layer:
        array: List[Layer] = []
        for layerFromDict in dictionary.values():
            tensor: TensorflowNetworkLayer = layerFromDict
            array.append(tensor.value)
        return tf.concat(
              axis=1, values=[*array])

    @classmethod
    def _return_tensor(cls, tensor):
        return tensor

    @classmethod
    def convert_dict_to_array(cls, dictionary: Dict[str, Layer]) -> Layer:
        array: List[Layer] = []
        for layerFromDict in dictionary.values():
            array.append(layerFromDict)
        return tf.concat(
            axis=1, values=[*array])
