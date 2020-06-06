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

    def generate_spent_time_award(self,
                                  current_game_state: GameState,
                                  last_game_state: GameState) -> float:
        result: float = 0
        return result

    def generate_speed_award(self,
                             current_game_state: GameState,
                             last_game_state: GameState) -> float:
        result: float = 0
        return result

