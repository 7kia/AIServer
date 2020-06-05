import json
import unittest

from src.ai.ai_commands import Json
from src.ai.ai_data_and_info.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.ai_logger import AiLogger
from src.ai.ai_data_and_info.ai_logger_builder_director import AiLoggerBuilderDirector
from src.ai.ai_data_and_info.ai_option import AiOption
from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.game_components.game_state import GameState


class TestLoggerCreator(unittest.TestCase):
    def setUp(self):
        self.logger: AiLogger = TestLoggerCreator.create_test_logger()

    @classmethod
    def create_test_logger(cls) -> AiLogger:
        director: AiLoggerBuilderDirector = AiLoggerBuilderDirector()
        ai_info = AiInfo("neuron-network", "scout-network")
        game_id = 1
        player_id = 2
        ai_option = AiOption()
        ai_option.troopType = "motorized"
        ai_option.is_train = True
        game_info = GameInfo(game_id, player_id, ai_option)

        return director.create_ai_logger(ai_info, game_info)


class AiLoggerConstructor(TestLoggerCreator):
    def test_have_file_with_game_record(self):
        self.assertEqual(self.logger.get_game_log_file_path() != "", True)

    def test_have_file_with_end_game_state(self):
        self.assertEqual(self.logger.get_end_game_state_file_path() != "", True)


class AiLoggerSaveToFileWithGameRecord(TestLoggerCreator):
    def setUp(self):
        super().setUp()
        self.awards: AiAwards = AiAwards()
        self.game_state: GameState = GameState()
        self.game_state.current_time = "0"
        self.logger.save_to_game_record_file(self.awards, self.game_state)

        self.game_state2: GameState = GameState()
        self.game_state2.current_time = "1"
        self.logger.save_end_game_state(self.awards, self.game_state2)


class CanSaveToFileWithGameRecord(AiLoggerSaveToFileWithGameRecord):
    def setUp(self):
        super().setUp()
        game_log = open(self.logger.get_game_log_file_path(), 'r')
        print(type(game_log))  # TODO 7kia удалить позже
        self.game_log_content: Json = json.load(game_log)

    def test_game_state(self):
        self.assertEqual(self.game_log_content["data"][0]["game_state"], self.game_state.as_json())
        self.assertEqual(self.game_log_content["data"][1]["game_state"], self.game_state2.as_json())

    def test_awards_for_the_state(self):
        self.assertEqual(self.game_log_content["data"][0]["awards"], self.awards.as_json())
        self.assertEqual(self.game_log_content["data"][1]["awards"], self.awards.as_json())


class AiLoggerSaveToFileWithEndGameState(TestLoggerCreator):
    def setUp(self):
        super().setUp()
        self.awards: AiAwards = AiAwards()
        self.awards.troop_amount = 1
        self.awards.experience = 2
        self.awards.organization = 3
        self.awards.overlap = 4

        self.game_state: GameState = GameState()
        self.game_duration: int = 4
        self.game_state.current_time = str(self.game_duration)

        for i in range(self.game_duration - 1):
            game_state: GameState = GameState()
            game_state.current_time = str(i)
            self.logger.save_to_game_record_file(self.awards, game_state)

        self.logger.save_end_game_state(self.awards, self.game_state)


class CanSaveToFileWithEndGameState(AiLoggerSaveToFileWithEndGameState):
    def setUp(self):
        super().setUp()
        game_log = open(self.logger.get_end_game_state_file_path(), 'r')
        print(type(game_log))  # TODO 7kia удалить позже
        self.game_log_content: Json = json.load(game_log)

        self.check_state: int = self.game_duration

    def test_game_state(self):
        self.assertEqual(self.game_log_content["game_state"],
                         self.game_state.as_json())

    def test_awards_for_the_state(self):
        self.assertEqual(self.game_log_content["awards"],
                         self.awards.as_json())

    def test_game_duration(self):
        self.assertEqual(self.game_log_content["game_duration"],
                         str(self.game_duration))

    def test_awards_sum_for_whole_game(self):
        self.assertEqual(self.game_log_content["awards_sum"], {
            "troop_amount": 1 * self.game_duration,
            "experience": 2 * self.game_duration,
            "organization": 3 * self.game_duration,
            "overlap": 4 * self.game_duration,
        })


if __name__ == '__main__':
    unittest.main()
