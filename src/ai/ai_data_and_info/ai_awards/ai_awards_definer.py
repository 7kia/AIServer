from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams
from src.ai.game_components.game_state import GameState


class AiAwardsDefiner:
    def __init__(self, awards_definer_params: AwardsDefinerParams):
        self.awards_definer_params: AwardsDefinerParams = awards_definer_params
        self._coefficient_composition_generalization: float = 0
        self._coefficient_organization_generalization: float = 0

    def get_coefficient_composition_generalization(self) -> float:
        return self._coefficient_composition_generalization

    def set_coefficient_composition_generalization(self, value: float):
        self._coefficient_composition_generalization = value

    def get_coefficient_organization_generalization(self) -> float:
        return self._coefficient_organization_generalization

    def set_coefficient_organization_generalization(self, value: float):
        self._coefficient_organization_generalization = value

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
        own_composition_t_last: float = last_game_state.person_unit_params.troopAmount
        own_composition_t: float = current_game_state.person_unit_params.troopAmount
        own_composition_different: float = own_composition_t_last - own_composition_t

        enemy_composition_t_last: float = last_game_state.person_unit_params.enemy_troop_amount
        enemy_composition_t: float = current_game_state.person_unit_params.enemy_troop_amount
        enemy_composition_different: float = enemy_composition_t_last - enemy_composition_t

        return self._coefficient_composition_generalization * (
            enemy_composition_different - own_composition_different
        )

    def generate_organization_award(self,
                                    current_game_state: GameState,
                                    last_game_state: GameState) -> float:
        own_organization_t_last: float = last_game_state.person_unit_params.organization
        own_organization_t: float = current_game_state.person_unit_params.organization
        own_organization_different: float = own_organization_t_last - own_organization_t

        enemy_organization_t_last: float = last_game_state.person_unit_params.enemy_organization
        enemy_organization_t: float = current_game_state.person_unit_params.enemy_organization
        enemy_organization_different: float = enemy_organization_t_last - enemy_organization_t

        return self._coefficient_organization_generalization * (
            enemy_organization_different - own_organization_different
        )

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
