import unittest

from src.ai.ai import Ai
from src.ai.ai_builder_director import AiBuilderDirector
from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_director import AiAwardsDefinerDirector
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_for_time_dependent_task import \
    AiAwardsDefinerForTimeDependentTask
from src.ai.ai_data_and_info.ai_awards.ai_awards_for_time_dependent_task import AiAwardsForTimeDependentTask
from src.ai.ai_data_and_info.ai_awards.awards_definer_params_extractor import AwardsDefinerParamsExtractor
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.ai_option import AiOption
from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.game_components.convert_self_to_json import Json
from src.ai.game_components.game_data_extractor import GameDataExtractor
from src.ai.game_components.game_state import GameState
from src.ai.game_components.person_unit_params import PersonUnitParams


class GenerateSimpleAiAwards(unittest.TestCase):
    def setUp(self) -> None:
        ai: Ai = self.create_test_ai()
        self.set_ai(ai)
        self._ai_awards_definer_director = AiAwardsDefinerDirector()
        ai_awards_definer: AiAwardsDefiner = self._ai_awards_definer_director.create_for_ai(ai)
        self.awards: AiAwards = ai_awards_definer.get_awards(
            ai.get_current_game_state(),
            ai.get_last_game_state()
        )
        self.json_awards: Json = self.awards.as_json()

    @classmethod
    def create_test_ai(cls) -> Ai:
        ai_info = AiInfo("neuron-network", "neuron-network")
        game_id = 1
        player_id = 2
        ai_option = AiOption()
        ai_option.troopType = "motorized"
        ai_option.is_train = True
        game_info = GameInfo(game_id, player_id, ai_option)
        ai: Ai = AiBuilderDirector.create_ai(ai_info, game_info)
        ai.set_awards_definer_params(AwardsDefinerParamsExtractor.extract({
            "ownUnitAmount": 4,
            "enemyUnitAmount": 3,
            "ownUnitCompositionAmount": 10,
            "enemyUnitCompositionAmount": 11
        }))
        return ai

    @classmethod
    def set_ai(cls, ai: Ai):
        ai.set_current_game_state(cls.generate_current_state())
        ai.set_last_game_state(cls.generate_last_state())

    @classmethod
    def generate_current_state(cls) -> GameState:
        game_state: GameState = GameState()
        person_unit_params: PersonUnitParams = PersonUnitParams()
        person_unit_params.troop_amount = 2
        person_unit_params.organization = 3
        person_unit_params.enemy_troop_amount = 3
        person_unit_params.enemy_organization = 3
        person_unit_params.experience = 4
        person_unit_params.overlap = 5

        game_state.person_unit_params = person_unit_params
        return game_state

    @classmethod
    def generate_last_state(cls) -> GameState:
        game_state: GameState = GameState()
        person_unit_params: PersonUnitParams = PersonUnitParams()
        person_unit_params.troop_amount = 1
        person_unit_params.organization = 1
        person_unit_params.enemy_troop_amount = 1
        person_unit_params.enemy_organization = 1

        person_unit_params.experience = 1
        person_unit_params.overlap = 1

        game_state.person_unit_params = person_unit_params
        return game_state
    
    # r = ρ×((enemy_hitpoint__t−1 – enemy_hitpoint__t)
    # - (unit_hitpoint__t−1 – unit_hitpoint__t))
    # имеется ввиду максимальное количество \/
    # ρ = Integral(enemy_hitpoint)/Integral(unit_hitpoint)
    def test_have_award_for_composition_or_health_points(self):
        self.assertEqual(3 / 4 * (11 - 10), self.json_awards["troop_amount"])

    def test_have_award_for_organization(self):
        self.assertEqual(2, self.json_awards["organization"])

    # rt = (unit_experiencet – unit_experiencet−1) / (unit_experiencet * unit_amount)
    def test_have_award_for_experience(self):
        self.assertEqual(3, self.json_awards["experience"])

    # rt = - m * (unit_overlapt – unit_overlapt−1) / (unit_overlapt * unit_amount) (3)
    # m = коэффициент, который равен 3 если (unit_overlapt – unit_overlapt−1)
    # больше 0, иначе равен 1
    def test_have_award_for_overlap(self):
        self.assertEqual(4, self.json_awards["overlap"])

    def test_can_summ_awards(self):
        test_awards: AiAwards = AiAwards()
        test_awards.troop_amount = 1
        test_awards.organization = 1
        test_awards.experience = 1
        test_awards.overlap = 1
        self.awards += test_awards
        self.assertEqual(2, self.awards.troop_amount)
        self.assertEqual(3, self.awards.organization)
        self.assertEqual(4, self.awards.experience)
        self.assertEqual(5, self.awards.overlap)


class GenerateNextAwardsOnlyForScoutAndRetreatNetworks(GenerateSimpleAiAwards):
    def setUp(self) -> None:
        super().setUp()

    @classmethod
    def create_test_ai(cls) -> Ai:
        ai_info = AiInfo("neuron-network", "scout-layer")
        game_id = 1
        player_id = 2
        ai_option = AiOption()
        ai_option.troopType = "motorized"
        ai_option.is_train = True
        game_info = GameInfo(game_id, player_id, ai_option)
        ai: Ai = AiBuilderDirector.create_ai(ai_info, game_info)
        ai.set_awards_definer_params(AwardsDefinerParamsExtractor.extract({
            "ownUnitAmount": 4,
            "enemyUnitAmount": 3,
            "ownUnitCompositionAmount": 10,
            "enemyUnitCompositionAmount": 11
        }))
        return ai

    @classmethod
    def generate_current_state(cls) -> GameState:
        game_state: GameState = GameState()
        person_unit_params: PersonUnitParams = PersonUnitParams()
        person_unit_params.troop_amount = 2
        person_unit_params.organization = 3
        person_unit_params.experience = 4
        person_unit_params.overlap = 5
        person_unit_params.speed = 6
        person_unit_params.spent_time = 7

        game_state.person_unit_params = person_unit_params
        return game_state

    @classmethod
    def generate_last_state(cls) -> GameState:
        game_state: GameState = GameState()
        person_unit_params: PersonUnitParams = PersonUnitParams()
        person_unit_params.troop_amount = 1
        person_unit_params.organization = 1
        person_unit_params.experience = 1
        person_unit_params.overlap = 1
        person_unit_params.speed = 1
        person_unit_params.spent_time = 1

        game_state.person_unit_params = person_unit_params
        return game_state

    def test_have_awards_from_AiAwards(self):
        self.assertEqual(1, self.json_awards["troop_amount"])
        self.assertEqual(2, self.json_awards["organization"])
        self.assertEqual(3, self.json_awards["experience"])
        self.assertEqual(4, self.json_awards["overlap"])

    # rt = (relative_speedt – relative_speedt−1) / (relative_speedt * unit_amount)
    def test_have_award_for_speed(self):
        self.assertEqual(5, self.json_awards["speed"])

    # r = (timet - timet-1) * 1.2
    def test_have_award_for_spent_time(self):
        self.assertEqual(6, self.json_awards["spent_time"])

    def test_can_summ_awards(self):
        test_awards: AiAwardsForTimeDependentTask = AiAwardsForTimeDependentTask()
        test_awards.troop_amount = 1
        test_awards.organization = 1
        test_awards.experience = 1
        test_awards.overlap = 1
        test_awards.speed = 1
        test_awards.spent_time = 1  
        self.awards += test_awards
        awards = self.awards
        self.assertEqual(2, awards.troop_amount)
        self.assertEqual(3, awards.organization)
        self.assertEqual(4, awards.experience)
        self.assertEqual(5, awards.overlap)
        self.assertEqual(6, awards.speed)
        self.assertEqual(7, awards.spent_time)

if __name__ == '__main__':
    unittest.main()
