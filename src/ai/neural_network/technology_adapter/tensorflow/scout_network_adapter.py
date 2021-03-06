from typing import List, Dict

from tensorflow.python.layers.base import Layer

from src.ai.game_components.command_data_generation import CommandDataGeneration
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation
from src.ai.neural_network.technology.tensorflow.networks.scout_network import ScoutNetwork
from src.ai.neural_network.technology_adapter.ai_command import AiCommand
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter
from src.ai.ai_command_generator import Json
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer, NetworkLayers
from src.ai.neural_network.technology_adapter.optimizer import Optimizer
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer
from src.ai.neural_network.technology_adapter.tensorflow.tensor_generator import TensorGenerator


class ScoutNetworkAdapter(NetworkAdapter):
    def __init__(self):
        super().__init__()
        self._network: ScoutNetwork = ScoutNetwork()

    def train(self,
              unit_observation: UnitObservation,
              current_game_state: GameState) -> AiCommand:
        result: AiCommand = self._network.train(
            unit_observation,
            current_game_state,
        )
        return result

    def test(self,
             unit_observation: UnitObservation,
             current_game_state: GameState) -> AiCommand:
        result: AiCommand = self._network.test(
            unit_observation,
            current_game_state,
        )
        return result

    def compile(self, optimizer: Optimizer, loss: ErrorFunction):
        self._network.compile(optimizer, loss)

    # TODO 7kia должен быть IAiAdapter и IAiAdapterSetter
    def set_input_layers(self, layers: Dict[str, NetworkLayers]):
        self._network.set_input_layers(self._convert_to_tensor_list(layers))

    def set_input_param_cost_definer(self, layers: NetworkLayers):
        self._network.set_input_param_cost_definer(self._extract_tensor_dict(layers))

    def set_command_cost_definer(self, layers: Dict[str, NetworkLayers]):
        self._network.set_command_cost_definer(self._convert_to_tensor_dict(layers))

    def set_command_definer(self, layers: NetworkLayer):
        self._network.set_command_definer(self._extract_tensor(layers))

    def set_output_layer(self, layers: NetworkLayers):
        self._network.set_output_layer(self._extract_tensor_dict(layers))

    @classmethod
    def _convert_to_tensor_dict(cls, layers: Dict[str, NetworkLayers]) -> Dict[str, Layer]:
        result: Dict[str, Layer] = {}
        for key in layers.keys():
            layer_list: NetworkLayers = layers[key]
            tensor_dict: Dict[str, Layer] = cls._extract_tensor_dict(layer_list)
            for tensor_key in tensor_dict:
                result[tensor_key] = tensor_dict[tensor_key]
        return result

    @classmethod
    def _convert_to_tensor_list(cls, layers: Dict[str, NetworkLayers]) -> List[Layer]:
        result: List[Layer] = []
        for key in layers.keys():
            layer_list: NetworkLayers = layers[key]
            tensor_dict: Dict[str, Layer] = cls._extract_tensor_dict(layer_list)
            for tensor_key in tensor_dict:
                result.append(tensor_dict[tensor_key])
        return result

    @staticmethod
    def _extract_tensor_dict(layers: NetworkLayers) -> Dict[str, Layer]:
        result: Dict[str, Layer] = {}
        for key in layers.keys():
            tensor: TensorflowNetworkLayer = layers[key]
            result[key] = tensor.value
        return result

    @staticmethod
    def _extract_tensor(layer: NetworkLayer) -> Layer:
        tensor: TensorflowNetworkLayer = layer
        return tensor.value

    def exist_model(self) -> bool:
        return self._network.exist_model()
