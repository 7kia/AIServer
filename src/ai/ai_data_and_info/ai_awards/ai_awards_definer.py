from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams
from src.ai.game_components.game_state import GameState


class AiAwardsDefiner:
    def __init__(self, awards_definer_params: AwardsDefinerParams):
        self.awards_definer_params: AwardsDefinerParams = awards_definer_params

    def get_awards(self, current_game_state: GameState,
                   last_game_state: GameState) -> AiAwards:
        awards: AiAwards = AiAwards()
        self._set_ai_awards_property(awards, current_game_state, last_game_state)
        return awards

    def _set_ai_awards_property(self, awards: AiAwards,
                                current_game_state: GameState,
                                last_game_state: GameState):
        awards.troop_amount = self.generate_troop_amount_award(current_game_state, last_game_state)
        awards.organization = self.generate_organization_award(current_game_state, last_game_state)
        awards.experience = self.generate_experience_award(current_game_state, last_game_state)
        awards.overlap = self.generate_overlap_award(current_game_state, last_game_state)

    def generate_troop_amount_award(self,
                                    current_game_state: GameState,
                                    last_game_state: GameState) -> float:
        result: float = 0
        return result

    def generate_organization_award(self,
                                    current_game_state: GameState,
                                    last_game_state: GameState) -> float:
        result: float = 0
        return result

    def generate_experience_award(self,
                                  current_game_state: GameState,
                                  last_game_state: GameState) -> float:
        result: float = 0
        return result

    def generate_overlap_award(self,
                               current_game_state: GameState,
                               last_game_state: GameState) -> float:
        result: float = 0
        return result
