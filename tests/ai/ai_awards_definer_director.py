import unittest

from src.ai.ai import Ai
from src.ai.ai_builder_director import AiBuilderDirector
from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_director import AiAwardsDefinerDirector
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_for_time_dependent_task import \
    AiAwardsDefinerForTimeDependentTask
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.ai_option import AiOption
from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.game_components.convert_self_to_json import Json
from src.ai.game_components.game_data_extractor import GameDataExtractor


class GenerateSimpleAiAwards(unittest.TestCase):
    def setUp(self) -> None:
        ai: Ai = self.create_test_ai()
        self.set_ai(ai)
        ai_awards_definer: AiAwardsDefiner = AiAwardsDefinerDirector.create_for_ai(ai)
        self.json_awards: Json = ai_awards_definer.get_awards(
            ai.get_current_game_state(),
            ai.get_last_game_state()
        ).as_json()

    @classmethod
    def create_test_ai(cls) -> Ai:
        ai_info = AiInfo("neuron-network", "neuron-network")
        game_id = 1
        player_id = 2
        ai_option = AiOption()
        ai_option.troopType = "motorized"
        ai_option.is_train = True
        game_info = GameInfo(game_id, player_id, ai_option)
        return AiBuilderDirector.create_ai(ai_info, game_info)

    @classmethod
    def set_ai(cls, ai: Ai):
        ai.set_current_game_state(GameDataExtractor.extract_game(cls.generate_current_state()))
        ai.set_last_game_state(GameDataExtractor.extract_game(cls.generate_last_state()))

    @classmethod
    def generate_current_state(cls) -> Json:
        return {}

    @classmethod
    def generate_last_state(cls) -> Json:
        return {}

    def test_have_award_for_composition_or_health_points(self):
        self.assertEqual(-1, self.json_awards["troop_amount"])

    def test_have_award_for_organization(self):
        self.assertEqual(-1, self.json_awards["organization"])

    def test_have_award_for_experience(self):
        self.assertEqual(-1, self.json_awards["experience"])

    def test_have_award_for_overlap(self):
        self.assertEqual(-1, self.json_awards["overlap"])


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
        return AiBuilderDirector.create_ai(ai_info, game_info)

    @classmethod
    def generate_current_state(cls) -> Json:
        return {}

    @classmethod
    def generate_last_state(cls) -> Json:
        return {}

    def test_have_awards_from_AiAwards(self):
        self.assertEqual(-1, self.json_awards["troop_amount"])
        self.assertEqual(-1, self.json_awards["organization"])
        self.assertEqual(-1, self.json_awards["experience"])
        self.assertEqual(-1, self.json_awards["overlap"])

    def test_have_award_for_speed(self):
        self.assertEqual(-1, self.json_awards["speed"])

    def test_have_award_for_spent_time(self):
        self.assertEqual(-1, self.json_awards["spent_time"])


if __name__ == '__main__':
    unittest.main()
