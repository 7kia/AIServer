from src.ai.neural_network.technology.tensorflow.networks.scout_network import ScoutNetwork
from src.ai.neural_network.technology_adapter.network_adapter import NetworkAdapter


class ScoutNetworkAdapter(NetworkAdapter):
    def __init__(self):
        super().__init__()
        self._network: ScoutNetwork = ScoutNetwork()

    def train(self):
        pass

    def test(self):
        pass

    def set_layer_1(self, param):
        pass
