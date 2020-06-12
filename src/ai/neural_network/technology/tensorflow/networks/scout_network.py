from typing import List, Dict

from tensorflow import keras
from tensorflow import constant as TfConstant
from tensorflow import Variable as TfVariable
from tensorflow.keras import layers
from tensorflow.python.keras import Input
from tensorflow.python.keras.callbacks import History
from tensorflow.python.keras.losses import Loss
from tensorflow.python.keras.optimizers import Optimizer
from tensorflow.python.layers.base import Layer

from src.ai.game_components.command_data_generation import CommandDataGeneration
from src.ai.game_components.game_state import GameState
from src.ai.game_components.move_direction import MoveDirection
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology.tensorflow.networks.network_adapter import NetworkAdapter
from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction as MyErrorFunction
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer, NetworkLayers
from src.ai.neural_network.technology_adapter.optimizer import Optimizer as MyOptimizer
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class ScoutNetwork(NetworkAdapter):
    # слой определения ценности параметров
    __input_param_cost_definer: Dict[str, Layer] = None
    # слой определения ценности конкретной команды
    __command_cost_definer: Dict[str, Layer] = None
    # слой объединения значений и определения выходной окманды
    __command_definer: Layer = None

    _current_game_state: TfVariable = None
    _last_game_state: TfVariable = None
    def __init__(self):
        super().__init__()
        # https://github.com/maurock/snake-ga/blob/master/DQN.py
        # self._input_layer = Input(shape=(150, 150, 3))
        #
        # # для каждого поля из примитивных типов по 1 relu
        # x = layers.Dense(64, activation='relu', name='dense_1')(self._input_layer)
        #
        # self._output_layer: Layer = layers.Dense(10, name='predictions')(x)

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
              unit_observation: TfConstant,
              current_game_state: TfConstant) -> AiCommand:
        history: History = self._final_model.fit(
            unit_observation, current_game_state,
            batch_size=1
        )
        print('\nhistory dict:', history.history)
        return self.test(unit_observation, current_game_state)

    def test(self,
             unit_observation: TfConstant,
             current_game_state: TfConstant) -> AiCommand:
        self._set_current_and_last_game_state(current_game_state)

        unit_observation_data: UnitObservation = unit_observation.read_value()
        current_game_state: GameState = current_game_state.read_value()

        unit_observation_data.own_organization
        unit_observation_data.own_composition
        unit_observation_data.sector
        unit_observation_data.own_sum_info
        unit_observation_data.own_max_info
        unit_observation_data.enemy_sum_info
        unit_observation_data.enemy_max_info

        current_game_state.person_unit_params.troop_amount
        current_game_state.person_unit_params.organization
        current_game_state.person_unit_params.enemy_troop_amount
        current_game_state.person_unit_params.enemy_organization
        current_game_state.person_unit_params.experience
        current_game_state.person_unit_params.overlap
        current_game_state.person_unit_params.speed

        current_game_state.sector_params.own_sum_info
        current_game_state.sector_params.own_max_info
        current_game_state.sector_params.enemy_sum_info
        current_game_state.sector_params.enemy_max_info

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

    def set_input_param_cost_definer(self, layer: Dict[str, Layer]):
        self.__input_param_cost_definer = layer

    def set_command_cost_definer(self, layer: Dict[str, Layer]):
        self.__command_cost_definer = layer

    def _set_current_and_last_game_state(self, current_game_state: TfConstant):
        if self._current_game_state is None:
            self._current_game_state = current_game_state
        self._last_game_state = self._current_game_state
        self._current_game_state = current_game_state

    def set_command_definer(self, layer: Layer):
        self.__command_definer = layer
