from src.ai.neural_network.technology.tensorflow.networks.network_adapter import NetworkAdapter
from typing import List

from src.ai.ai_commands import Json


class ScoutNetwork(NetworkAdapter):
    def __init__(self):
        super().__init__()
        self.layer = None

    def train(self) -> List[Json]:
        pass

    def test(self) -> List[Json]:
        pass
