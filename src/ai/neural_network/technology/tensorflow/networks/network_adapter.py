from enum import Enum
from typing import List, Dict

from tensorflow import constant
from tensorflow.python.layers.base import Layer

from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from tensorflow.python.keras.models import Model

from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


# TODO 7kia дублирование из-за того что не видит из модуля с director-ом
class InputLayerNames(Enum):
    unit_observation: str = "unit_observation"
    person_unit_params: str = "person_unit_params"
    sector_params: str = "sector_params"


class InputParamCostDefinerLayerNames(Enum):
    unit_observation: str = "unit_observation__cost_definer"
    person_unit_params: str = "person_unit_params__cost_definer"
    sector_params: str = "sector_params__cost_definer"


class CommandCostDefinerLayerNames(Enum):
    unit_observation: str = "unit_observation__command_cost_definer"
    person_unit_params: str = "person_unit_params__command_cost_definer"
    sector_params: str = "sector_params__command_cost_definer"


command_cost_definer_layer_names: List[CommandCostDefinerLayerNames] = []
for name in CommandCostDefinerLayerNames:
    command_cost_definer_layer_names.append(name)


class CommandCostDefinerTensorNames(Enum):
    up: str = "up_command_cost_definer"
    up_right: str = "up_right_command_cost_definer"
    right: str = "right_command_cost_definer"
    down_right: str = "down_right_command_cost_definer"
    down: str = "down_command_cost_definer"
    down_left: str = "down_left_command_cost_definer"
    left: str = "left_command_cost_definer"
    up_left: str = "up_left_command_cost_definer"


command_cost_definer_tensor_names: List[CommandCostDefinerTensorNames] = []
for name in CommandCostDefinerTensorNames:
    command_cost_definer_tensor_names.append(name)


class CommandCostDefinerTensorId(Enum):
    up: int = 0
    up_right: int = 1
    right: int = 2
    down_right: int = 3
    down: int = 4
    down_left: int = 5
    left: int = 6
    up_left: int = 7


class CommandDefinerLevel(Enum):
    command_cost_summation_layer: str = "command_cost_summation_layer"
    result: str = "result_layer"

class NetworkAdapter:
    _input_layer: List[Layer] = None
    _output_layer: Dict[str, Layer] = None
    _final_model: Model = None

    def __init__(self):
        pass

    def train(self,
              unit_observation: UnitObservation,
              current_game_state: GameState) -> AiCommand:
        pass

    def test(self,
             unit_observation: UnitObservation,
             current_game_state: GameState) -> AiCommand:
        pass

    def set_input_layers(self, input_layer: List[Layer]):
        self._input_layer = input_layer

    def set_output_layer(self, output_layer: Dict[str, Layer]):
        self._output_layer = output_layer

    def _convert_dict_array(self, input_layer: Dict[str, Layer]) -> List[Layer]:
        result: List[Layer] = []
        for value in input_layer.values():
            result.append(value)
        return result

