from tensorflow.python.layers.base import Layer

from src.ai.neural_network.technology_adapter.network_layer import NetworkLayer


class TensorflowNetworkLayer(NetworkLayer):
    value: Layer = None

    def __init__(self):
        super().__init__()


