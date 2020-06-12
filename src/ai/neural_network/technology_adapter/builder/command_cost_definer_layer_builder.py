from src.ai.neural_network.technology_adapter.network_layer import NetworkLayers, NetworkLayer


class CommandCostDefinerLayerBuilder:
    def generate_for_unit_observation_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        pass

    def generate_for_sector_params_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        pass

    def generate_for_person_unit_params_layer(self, input_layers: NetworkLayers) -> NetworkLayer:
        pass
