from typing import Dict

from src.ai.neural_network.technology_adapter.builder.command_cost_definer_layer_builder import \
    CommandCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers, NetworkLayer
from src.ai.neural_network.technology_adapter.tensorflow.network_layer import TensorflowNetworkLayer


class TensorflowCommandCostDefinerLayerBuilder(CommandCostDefinerLayerBuilder):
    def __init__(self):
        super().__init__()

    def generate_command_cost_definer_unit_observation_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        result: Dict[str, TensorflowNetworkLayer] = {}
        return result

    def generate_command_cost_definer_sector_params_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        result: Dict[str, TensorflowNetworkLayer] = {}
        return result

    def generate_command_cost_definer_unit_params_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        result: Dict[str, TensorflowNetworkLayer] = {}
        return result
