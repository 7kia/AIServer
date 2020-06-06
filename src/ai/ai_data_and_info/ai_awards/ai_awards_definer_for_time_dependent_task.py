from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_awards.ai_awards_for_time_dependent_task import AiAwardsForTimeDependentTask
from src.ai.ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams
from src.ai.game_components.game_state import GameState


class AiAwardsDefinerForTimeDependentTask(AiAwardsDefiner):
    def __init__(self, awards_definer_params: AwardsDefinerParams):
        super().__init__(awards_definer_params)

    def get_awards(self, current_game_state: GameState,
                   last_game_state: GameState) -> AiAwards:
        awards: AiAwardsForTimeDependentTask = AiAwardsForTimeDependentTask()
        self._set_ai_awards_property(awards, current_game_state, last_game_state)
        awards.spent_time = self.generate_spent_time_award(current_game_state, last_game_state)
        awards.speed = self.generate_speed_award(current_game_state, last_game_state)
        return awards

    # r = (timet - timet-1) * 1.2
    def generate_spent_time_award(self,
                                  current_game_state: GameState,
                                  last_game_state: GameState) -> float:
        time_last: float = last_game_state.current_time.get_as_float()
        time: float = current_game_state.current_time.get_as_float()
        own_speed_different: float = (time_last - time) * 1.2
        return own_speed_different

    # rt = (relative_speedt – relative_speedt−1) / (relative_speedt * unit_amount)
    def generate_speed_award(self,
                             current_game_state: GameState,
                             last_game_state: GameState) -> float:
        own_speed_t_last: float = last_game_state.person_unit_params.speed
        own_speed_t: float = current_game_state.person_unit_params.speed
        own_speed_different: float = own_speed_t - own_speed_t_last

        return own_speed_different / (own_speed_t * self.awards_definer_params.own_unit_amount)

