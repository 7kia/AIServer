from tensorflow.python.keras.losses import Loss

from src.ai.neural_network.technology_adapter.tensorflow.tensorflow_error_function import TensorflowErrorFunction
import tensorflow as tf
from tensorflow import Variable as TfVariable


class ScoutNetworkLossFunction(Loss):
    def __init__(self, error_function: TensorflowErrorFunction):
        super().__init__()
        self.error_function: TensorflowErrorFunction = error_function

    def __call__(self, y_true, y_pred, sample_weight=None):
        return tf.Variable(self.error_function(y_true, y_pred, sample_weight))

    def set_game_states(self, current_game_state: TfVariable, last_game_state: TfVariable):
        self.error_function.set_game_states(
            current_game_state,
            last_game_state
        )
