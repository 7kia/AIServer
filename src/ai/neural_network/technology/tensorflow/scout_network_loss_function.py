import numpy as np
from tensorflow.python.keras.losses import Loss

from src.ai.neural_network.technology_adapter.tensorflow.tensorflow_error_function import TensorflowErrorFunction
import tensorflow as tf
from tensorflow import Variable as TfVariable


@tf.custom_gradient
def clip_gradients(x):
    # def backward(dx):
    #     return tf.clip_by_norm(dx, 0.1)

    def grad(dy, variables=None):
        return dy, [dy for v in variables]
    return tf.clip_by_norm(x, 0.1), grad    # x, backward


class ScoutNetworkLossFunction(Loss):
    def __init__(self, error_function: TensorflowErrorFunction):
        super().__init__()
        self.error_function: TensorflowErrorFunction = error_function

    def call(self, y_true=None, y_pred=None):
        value = self.error_function(y_true, y_pred)
        return np.asarray([float(-value)])


    def set_game_states(self, get_current_game_state, get_last_game_state):
        self.error_function.set_game_states(
            get_current_game_state,
            get_last_game_state
        )
