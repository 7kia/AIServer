import tensorflow as tf

from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.game_components.game_state import GameState
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction
import tensorflow as tf


class TensorflowErrorFunction(ErrorFunction):
    ai_awards_definer: AiAwardsDefiner = None
    _current_game_state: tf.Variable = None
    _last_game_state: tf.Variable = None

    def __init__(self, ai_awards_definer: AiAwardsDefiner):
        super().__init__()
        self.ai_awards_definer: AiAwardsDefiner = ai_awards_definer

    def set_game_states(self, current_game_state: tf.Variable, last_game_state: tf.Variable):
        self._current_game_state = current_game_state
        self._last_game_state = last_game_state

    def __call__(self, y_true, y_pred, sample_weight=None) -> float:
        awards: AiAwards = self.ai_awards_definer.get_awards(
            self._current_game_state.read_value(),
            self._last_game_state.read_value()
        )
        return awards.get_sum_award()
