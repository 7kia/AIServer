import unittest
from typing import List

from src.ai.ai_commands import Json, CommandName
from src.ai.script_bot import ScriptBot
from src.fortest import generate_mock_location_info, convert_dictionary_values_to_list
from src.fortest.test_data_generator import TestDataGenerator
from src.game import Game
from src.game_data_extractor import UnitList, UnitDict, GameDataExtractor
from src.unit import Unit, RegimentType, BaseType, SupportType


class CanChoiceRandomAmountUnits(unittest.TestCase):
    def test_choice_random_amount_units(self):
        unit_dictionary: UnitDict = TestDataGenerator.generate_test_unit_dictionary()
        choised_units: UnitList = ScriptBot.choose_random_units(unit_dictionary)

        if len(choised_units) > 0:
            all_units: List[Unit] = convert_dictionary_values_to_list(unit_dictionary)
            for unit in choised_units:
                self.assertIn(unit, all_units)




class CanReturnRandomCommandsWithRandomParameters(unittest.TestCase):
    def test_return_random_command_list_with_random_parameters(self):
        game_id: int = 3
        player_id: int = 31
        bot_country: str = "Ukraine"
        script_bot: ScriptBot = self.generate_test_script_bot(
            game_id, player_id, bot_country
        )
        game: Game = TestDataGenerator.generate_test_game(
            game_id, player_id
        )
        commands: List[Json] = script_bot.get_commands(game)
        self.assertEqual(True, self.is_the_commands_to(commands, self.generate_list_existing_commands()))

    @staticmethod
    def generate_test_script_bot(game_id: int, player_id: int, bot_country: str) -> ScriptBot:
        input_data: dict[str, any] = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": "script-bot",
            "ai_name": "intellectual-000",
            "location": generate_mock_location_info(),
            "country": bot_country,
        }
        script_bot: ScriptBot = ScriptBot()
        script_bot.set_location(input_data["location"])
        script_bot.set_country(input_data["country"])
        return script_bot



    @staticmethod
    def is_the_commands_to(commands: List[Json], expected_commands: List[str]) -> bool:
        for command in commands:
            if command["commandName"] in expected_commands:
                return True
        return False

    @staticmethod
    def generate_list_existing_commands() -> List[str]:
        result: List[str] = []
        for command_name in CommandName:
            result.append(command_name.value.__str__())
        return result


if __name__ == '__main__':
    unittest.main()
