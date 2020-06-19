from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.neural_network.technology_adapter.error_function import ErrorFunction


class TensorflowErrorFunction(ErrorFunction):
    ai_awards_definer: AiAwardsDefiner = None
    _get_current_game_state = None
    _get_last_game_state = None

    def __init__(self, ai_awards_definer: AiAwardsDefiner):
        super().__init__()
        self.ai_awards_definer: AiAwardsDefiner = ai_awards_definer

    def set_game_states(self, get_current_game_state, get_last_game_state):
        self._get_current_game_state = get_current_game_state
        self._get_last_game_state = get_last_game_state

    def __call__(self, y_true=None, y_pred=None) -> float:
        if self._get_current_game_state() is None:
            return 0
        awards: AiAwards = self.ai_awards_definer.get_awards(
            self._get_current_game_state().read_value(),
            self._get_last_game_state().read_value()
        )
        return awards.get_sum_award()
