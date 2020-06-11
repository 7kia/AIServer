from typing import List

from tensorflow import constant
from tensorflow.python.layers.base import Layer

from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from tensorflow.python.keras.models import Model

from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class NetworkAdapter:
    _input_layer: Layer = None
    _output_layer: Layer = None
    _final_model: Model = None

    def __init__(self):
        pass

    def train(self,
              unit_observation: constant,
              current_game_state: constant) -> AiCommand:
        pass

    def test(self,
             unit_observation: constant,
             current_game_state: constant,) -> AiCommand:
        pass

    def set_input_layers(self, input_layer: List[NetworkLayer]):
        layer: TensorflowNetworkLayer = input_layer
        self._input_layer = layer.value

    def set_output_layer(self, output_layer: NetworkLayer):
        layer: TensorflowNetworkLayer = output_layer
        self._output_layer = layer.value
