from tensorflow import keras
from tensorflow.python.keras.models import Model
from tensorflow.python.layers.base import Layer

from src.ai.neural_network.technology.tensorflow.networks.network_adapter import NetworkAdapter
from typing import List

from src.ai.ai_commands import Json
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction as MyErrorFunction
from src.ai.neural_network.technology_adapter.optimizer import Optimizer as MyOptimizer


class ScoutNetwork(NetworkAdapter):
    _input_layer: Layer = None
    _output_layer: Layer = None
    _final_model: Model = None

    _layer: Layer = None

    def __init__(self):
        super().__init__()

    # def __init__(self):
    #     super(MyModel, self).__init__()
    #     self.conv1 = Conv2D(32, 3, activation='relu')
    #     self.flatten = Flatten()
    #     self.d1 = Dense(128, activation='relu')
    #     self.d2 = Dense(10, activation='softmax')
    #
    # def call(self, x):
    #     x = self.conv1(x)
    #     x = self.flatten(x)
    #     x = self.d1(x)
    #     return self.d2(x)

    def train(self) -> List[Json]:
        self._final_model.fit()

    def test(self) -> List[Json]:
        result: List[Json] = []

        return result

    def compile(self,  optimizer: MyOptimizer, loss: MyErrorFunction):
        self._final_model = keras.Model(inputs=self._input_layer, outputs=self._output_layer)
