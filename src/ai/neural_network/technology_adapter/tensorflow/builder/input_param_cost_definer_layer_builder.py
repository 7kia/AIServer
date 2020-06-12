from src.ai.neural_network.technology_adapter.builder.input_param_cost_definer_layer_builder import \
    InputParamCostDefinerLayerBuilder
from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers, NetworkLayer


class TensorflowInputParamCostDefinerLayerBuilder(InputParamCostDefinerLayerBuilder):
    def __init__(self):
        super().__init__()

    def generate_input_param_cost_definer_unit_observation_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        pass

    def generate_input_param_cost_definer_sector_params_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        pass

    def generate_input_param_cost_definer_unit_params_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        pass
