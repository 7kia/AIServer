from typing import List

from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams
from src.ai.game_components.game_state import GameState
from src.ai.game_components.sector_params import UnitMatrix
from src.ai.game_components.unit import Unit


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
        awards.unit_detection = self.generate_unit_detection_award(current_game_state, last_game_state)

    def generate_troop_amount_award(self,
                                    current_game_state: GameState,
                                    last_game_state: GameState) -> float:
        own_composition_t_last: float = last_game_state.person_unit_params.troop_amount
        own_composition_t: float = current_game_state.person_unit_params.troop_amount
        own_composition_different: float = own_composition_t - own_composition_t_last

        enemy_composition_t_last: float = last_game_state.person_unit_params.enemy_troop_amount
        enemy_composition_t: float = current_game_state.person_unit_params.enemy_troop_amount
        enemy_composition_different: float = enemy_composition_t - enemy_composition_t_last

        return self._coefficient_composition_generalization * (
                own_composition_different - enemy_composition_different
        )

    def generate_organization_award(self,
                                    current_game_state: GameState,
                                    last_game_state: GameState) -> float:
        own_organization_t_last: float = last_game_state.person_unit_params.organization
        own_organization_t: float = current_game_state.person_unit_params.organization
        own_organization_different: float = own_organization_t - own_organization_t_last

        enemy_organization_t_last: float = last_game_state.person_unit_params.enemy_organization
        enemy_organization_t: float = current_game_state.person_unit_params.enemy_organization
        enemy_organization_different: float = enemy_organization_t - enemy_organization_t_last

        return self._coefficient_organization_generalization * (
                own_organization_different - enemy_organization_different
        )

    # rt = (unit_experiencet – unit_experiencet−1) / (unit_experiencet * unit_amount)
    def generate_experience_award(self,
                                  current_game_state: GameState,
                                  last_game_state: GameState) -> float:
        own_experience_t_last: float = last_game_state.person_unit_params.experience
        own_experience_t: float = current_game_state.person_unit_params.experience
        own_experience_different: float = own_experience_t - own_experience_t_last
        return own_experience_different / (own_experience_t * self.awards_definer_params.own_unit_amount)

    # rt = - m * (unit_overlapt – unit_overlapt−1) / (unit_overlapt * unit_amount) (3)
    # m = коэффициент, который равен 3 если (unit_overlapt – unit_overlapt−1)
    # больше 0, иначе равен 1
    def generate_overlap_award(self,
                               current_game_state: GameState,
                               last_game_state: GameState) -> float:
        own_overlap_t_last: float = last_game_state.person_unit_params.overlap
        own_overlap_t: float = current_game_state.person_unit_params.overlap
        own_overlap_different: float = own_overlap_t - own_overlap_t_last

        overlap_coefficient: float = self._generate_overlap_coefficient(own_overlap_different)
        return overlap_coefficient * own_overlap_different \
               / (own_overlap_t * self.awards_definer_params.own_unit_amount)

    @staticmethod
    def _generate_overlap_coefficient(own_overlap_different: float) -> float:
        result: float = 1
        if own_overlap_different > 0:
            return -3
        return result

    def generate_unit_detection_award(self,
                                      current_game_state: GameState,
                                      last_game_state: GameState) -> float:
        current_unit_to_sectors: UnitMatrix = current_game_state.sector_params.enemyUnitToSectors
        last_unit_to_sectors: UnitMatrix = last_game_state.sector_params.enemyUnitToSectors
        result: float = 50.0 * self._get_new_enemies_amount(current_unit_to_sectors, last_unit_to_sectors)
        return result

    @staticmethod
    def _get_new_enemies_amount(current_unit_to_sectors: UnitMatrix,
                                last_unit_to_sectors: UnitMatrix) -> int:
        result: int = 0
        matrix_size: int = len(current_unit_to_sectors[0])
        for row_index in range(matrix_size):
            for cell_index in range(matrix_size):
                current_units: List[Unit] = current_unit_to_sectors[row_index][cell_index]
                last_units: List[Unit] = last_unit_to_sectors[row_index][cell_index]
                result += len(current_units) - len(last_units)
        return result
