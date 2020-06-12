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
              command_data_generation: CommandDataGeneration,
              unit_observation: UnitObservation,
              current_game_state: GameState) -> Json:
        command_numbers: AiCommand = self._network.train(
            TensorGenerator.generate_for_unit_observation(unit_observation),
            TensorGenerator.generate_for_game_state(current_game_state),
        )
        result: Json = self._convert_to_json(command_numbers, command_data_generation)
        return result

    def test(self,
             command_data_generation: CommandDataGeneration,
             unit_observation: UnitObservation,
             current_game_state: GameState) -> Json:
        command_numbers: AiCommand = self._network.test(
            TensorGenerator.generate_for_unit_observation(unit_observation),
            TensorGenerator.generate_for_game_state(current_game_state),
        )
        result: Json = self._convert_to_json(command_numbers, command_data_generation)
        return result

    def compile(self, optimizer: Optimizer, loss: ErrorFunction):
        self._network.compile(optimizer, loss)

    # TODO 7kia должен быть IAiAdapter и IAiAdapterSetter
    def set_input_layers(self, layers: NetworkLayers):
        self._network.set_input_layers(self._extract_tensor_dict(layers))

    def set_input_param_cost_definer(self, layers: NetworkLayers):
        self._network.set_input_param_cost_definer(self._extract_tensor_dict(layers))

    def set_command_cost_definer(self, layers: NetworkLayers):
        self._network.set_command_cost_definer(self._extract_tensor_dict(layers))

    def set_command_definer(self, layers: NetworkLayer):
        self._network.set_command_definer(self._extract_tensor(layers))

    def set_output_layer(self, layers: NetworkLayer):
        self._network.set_output_layer(self._extract_tensor(layers))

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
