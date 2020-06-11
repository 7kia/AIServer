from tensorflow import keras, constant
from tensorflow.keras import layers
from tensorflow.python.keras import Input
from tensorflow.python.keras.callbacks import History
from tensorflow.python.keras.losses import Loss
from tensorflow.python.keras.models import Model
from tensorflow.python.keras.optimizers import Optimizer
from tensorflow.python.layers.base import Layer

from src.ai.game_components.move_direction import MoveDirection
from src.ai.neural_network.technology.tensorflow.networks.network_adapter import NetworkAdapter
from typing import List

from src.ai.ai_command_generator import Json
from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction as MyErrorFunction
from src.ai.neural_network.technology_adapter.optimizer import Optimizer as MyOptimizer


class ScoutNetwork(NetworkAdapter):
    _input_layer: Layer = None
    _output_layer: Layer = None
    _final_model: Model = None

    _layer: Layer = None

    def __init__(self):
        super().__init__()
        # https://github.com/maurock/snake-ga/blob/master/DQN.py
        self._input_layer = Input(shape=(150, 150, 3))

        # для каждого поля из примитивных типов по 1 relu
        x = layers.Dense(64, activation='relu', name='dense_1')(self._input_layer)

        self._output_layer: Layer = layers.Dense(10, name='predictions')(x)

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
    def train(self,
              command_data_generation: constant,
              unit_observation: constant,
              current_game_state: constant,
              last_game_state: constant) -> AiCommand:
        history: History = self._final_model.fit(
            unit_observation, current_game_state,
            batch_size=1
        )
        print('\nhistory dict:', history.history)
        return self.test(command_data_generation, unit_observation, current_game_state)

    def test(self,
             command_data_generation: constant,
             unit_observation: constant,
             current_game_state: constant) -> AiCommand:
        direction: MoveDirection = None
        command_name: str = ""
        return AiCommand(direction, command_name)

    def compile(self, optimizer: MyOptimizer, loss: MyErrorFunction):
        new_optimizer: Optimizer = self._create_optimizer(optimizer)
        new_loss: Loss = self._create_loss(loss)
        self._final_model = keras.Model(inputs=self._input_layer, outputs=self._output_layer)
        self._final_model.compile(
            optimizer=new_optimizer,
            loss=new_loss,
            metrics=['accuracy'],
        )
