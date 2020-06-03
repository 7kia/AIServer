import json
import unittest
from typing import List

from src.ai.ai_builder_director import AiBuilderDirector
from src.ai.ai_commands import Json, CommandName
from src.ai.ai_data_and_info.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.ai_logger import AiLogger
from src.ai.ai_data_and_info.ai_logger_builder_director import AiLoggerBuilderDirector
from src.ai.ai_data_and_info.ai_option import AiOption
from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.script_bot import ScriptBot
from src.fortest import generate_mock_location_info, convert_dictionary_values_to_list
from src.fortest.test_data_generator import TestDataGenerator
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit import Unit, UnitList, UnitDict
from chai import Chai
from pocha import describe, it


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
        game_info = GameInfo(game_id, player_id, ai_option)

        return director.create_ai_logger(ai_info, game_info)


class AiLoggerConstructor(TestLoggerCreator):
    def test_have_file_with_game_record(self):
        self.assertEqual(True, False)

    def test_have_file_with_end_game_state(self):
        self.assertEqual(True, False)


class AiLoggerSaveToFileWithGameRecord(TestLoggerCreator):
    def setUp(self):
        super().setUp()
        # awards: AiAwards = AiAwards()
        # game_state: GameState = GameState()
        # self.logger.save_current_state(awards, game_state)
        # self.logger.save_current_state(awards, game_state)
        #
        # game_log = open(self.logger.get_game_log(), 'r')
        # print(type(game_log))
        # game_log_content: Json = json.load(game_log)

        self.assertEqual(True, False)


class CanSaveToFileWithGameRecord(AiLoggerSaveToFileWithGameRecord):
    def setUp(self):
        super().setUp()

    def test_game_state(self):
        self.assertEqual(True, False)

    def test_awards_for_the_state(self):
        self.assertEqual(True, False)


class AiLoggerSaveToFileWithEndGameState(TestLoggerCreator):
    def setUp(self):
        super().setUp()
        # awards: AiAwards = AiAwards()
        # game_state: GameState = GameState()
        # self.logger.save_current_state(awards, game_state)
        # self.logger.save_current_state(awards, game_state)
        #
        # game_log = open(self.logger.get_game_log(), 'r')
        # print(type(game_log))
        # game_log_content: Json = json.load(game_log)

        self.assertEqual(True, False)


class CanSaveToFileWithEndGameState(AiLoggerSaveToFileWithEndGameState):
    def test_game_state(self):
        self.assertEqual(True, False)

    def test_awards_for_the_state(self):
        self.assertEqual(True, False)

    def test_game_duration(self):
        self.assertEqual(True, False)

    def test_awards_sum_for_whole_game(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
