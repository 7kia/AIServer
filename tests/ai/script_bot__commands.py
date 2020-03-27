import unittest
from abc import ABC

from src.ai.ai_commands import Json, CommandName
from src.ai.script_bot import ScriptBot
from src.fortest import generate_mock_location_info, convert_dictionary_values_to_list
from src.fortest.test_data_generator import TestDataGenerator
from src.game_data_extractor import UnitDict
from src.location import Location
from src.unit import UnitList


class TestScriptBot(ScriptBot, ABC):
    def __init__(self):
        super().__init__()

    def generate_move_or_attack_command(self) -> Json:
        return self._generate_move_or_attack_command()

    def generate_retreat_or_storm_command(self) -> Json:
        return self._generate_retreat_or_storm_command()

    def generate_stop_or_defence_command(self) -> Json:
        return self._generate_stop_or_defence_command()

    def choice_random_position(self):
        return self._choice_random_position()

class CanGenerateCommandTestData:
    def __init__(self, bot: TestScriptBot, game_id: int, player_id: int):
        self.bot = bot
        self.game = TestDataGenerator.generate_test_game(
            game_id, player_id
        )

class CanGenerateCommands(unittest.TestCase):
    @staticmethod
    def generate_test_data() -> CanGenerateCommandTestData:
        game_id: int = 31
        player_id: int = 32
        bot_country: str = "Ukraine"
        return CanGenerateCommandTestData(
            CanGenerateCommands.generate_test_script_bot(game_id, player_id, bot_country),
            game_id, player_id,
        )

    @staticmethod
    def generate_test_script_bot(game_id: int, player_id: int, bot_country: str) -> TestScriptBot:
        input_data: dict[str, any] = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": "script-bot",
            "ai_name": "intellectual-000",
            "location": generate_mock_location_info(),
            "country": bot_country,
        }
        script_bot: TestScriptBot = TestScriptBot()
        script_bot.set_location(input_data["location"])
        script_bot.set_country(input_data["country"])
        return script_bot

    def test_generate_moveOrAttack_command(self):
        testData: CanGenerateCommandTestData = CanGenerateCommands.generate_test_data()

        command: Json = testData.bot\
            .generate_move_or_attack_command(testData.game)
        self.assertEqual(command["commandName"], CommandName.move_or_attack.value.__str__())
        self.assertEqual(
            True,
            TestsForCommandGenerationPrivateMethods.check_position(command)
        )
        self.assertEqual(
            True,
            TestsForCommandGenerationPrivateMethods.check_unit_id(command)
        )

    def test_generate_retreatOrStorm_command(self):
        script_bot: TestScriptBot = CanGenerateCommands.generate_test_script_bot()

        command: Json = script_bot.generate_retreat_or_storm_command()
        self.assertEqual(command["commandName"], CommandName.retreat_or_storm.value.__str__())
        self.assertEqual(
            True,
            TestsForCommandGenerationPrivateMethods.check_position(command)
        )
        self.assertEqual(
            True,
            TestsForCommandGenerationPrivateMethods.check_unit_id(command)
        )

    def test_generate_stopOrDefence_command(self):
        script_bot: TestScriptBot = CanGenerateCommands.generate_test_script_bot()

        command: Json = script_bot.generate_stop_or_defence_command()
        self.assertEqual(command["commandName"], CommandName.stop_or_defence.value.__str__())
        self.assertEqual(
            True,
            TestsForCommandGenerationPrivateMethods.check_unit_id(command)
        )


class TestsForCommandGenerationPrivateMethods(unittest.TestCase):
    def test_choice_random_unit(self):
        self.assertEqual(True, False)

    def test_choice_random_position(self):
        self.assertEqual(True, False)

    @staticmethod
    def check_unit_id(command: Json, unit_dictionary: UnitDict) -> bool:
        unit_list: UnitList = convert_dictionary_values_to_list(unit_dictionary)
        for unit in unit_list:
            if command["unit_id"] in unit.id:
                return True
        return False

    @staticmethod
    def check_position(command: Json, location: Location) -> bool:

        return False


if __name__ == '__main__':
    unittest.main()
