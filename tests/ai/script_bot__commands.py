import unittest
from abc import ABC
from typing import List

from src.ai.ai_commands import Json, CommandName
from src.ai.game_components.position import Position
from src.ai.script_bot import ScriptBot
from src.fortest import generate_mock_location_info, convert_dictionary_values_to_list
from src.fortest.test_data_generator import TestDataGenerator
from src.ai.game_components.game import Game
from src.ai.game_components.game_data_extractor import UnitDict
from src.ai.game_components.location import Location, Bounds
from src.ai.game_components.unit import UnitList, Unit
from src.ai.game_components.unit_state_extractor import UnitStatusFromJson


class TestScriptBot(ScriptBot, ABC):
    def __init__(self):
        super().__init__()

    def generate_move_or_attack_command(self, unit: Unit, game: Game) -> Json:
        return self._generate_move_or_attack_command(unit, game)

    def generate_retreat_or_storm_command(self, unit: Unit, game: Game) -> Json:
        return self._generate_retreat_or_storm_command(unit, game)

    def generate_stop_or_defence_command(self, unit: Unit, game: Game) -> Json:
        return self._generate_stop_or_defence_command(unit, game)

    def choice_random_position(self, unit_position: Position) -> Position:
        return self._choice_random_position(unit_position)


class CanGenerateCommandTestData:
    def __init__(self, bot: TestScriptBot, game_id: int, player_id: int):
        self.bot: TestScriptBot = bot
        self.game: Game = TestDataGenerator.generate_test_game(
            game_id, player_id, generate_unit_with_various_state=True, map_bounds=bot.get_location().bounds
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
        test_data: CanGenerateCommandTestData = CanGenerateCommands.generate_test_data()
        unit: Unit = test_data.game.unit_dictionary["regiment"][UnitStatusFromJson.UNIT_STATUS_STOP.value - 1]

        command: Json = test_data.bot \
            .generate_move_or_attack_command(unit, test_data.game)
        self.assertEqual(command["commandName"], CommandName.move_or_attack.value.__str__())
        self.assertEqual(
            True, TestsForCommandGenerationPrivateMethods
                .check_position(command, test_data.bot.get_location())
        )
        self.assertEqual(
            True, TestsForCommandGenerationPrivateMethods
                .check_unit_id(command, test_data.game.unit_dictionary)
        )

    def test_generate_retreatOrStorm_command(self):
        test_data: CanGenerateCommandTestData = CanGenerateCommands.generate_test_data()
        unit: Unit = test_data.game.unit_dictionary["regiment"][UnitStatusFromJson.UNIT_STATUS_ATTACK.value - 1]

        command: Json = test_data.bot \
            .generate_retreat_or_storm_command(unit, test_data.game)
        self.assertEqual(command["commandName"], CommandName.retreat_or_storm.value.__str__())
        self.assertEqual(
            True, TestsForCommandGenerationPrivateMethods
                .check_position(command, test_data.bot.get_location())
        )
        self.assertEqual(
            True, TestsForCommandGenerationPrivateMethods
                .check_unit_id(command, test_data.game.unit_dictionary)
        )

    def test_generate_stopOrDefence_command(self):
        test_data: CanGenerateCommandTestData = CanGenerateCommands.generate_test_data()
        unit: Unit = test_data.game.unit_dictionary["regiment"][UnitStatusFromJson.UNIT_STATUS_MARCH.value - 1]

        command: Json = test_data.bot \
            .generate_stop_or_defence_command(unit, test_data.game)
        self.assertEqual(command["commandName"], CommandName.stop_or_defence.value.__str__())
        self.assertEqual(
            True, TestsForCommandGenerationPrivateMethods
                .check_unit_id(command, test_data.game.unit_dictionary)
        )


class TestsForCommandGenerationPrivateMethods(unittest.TestCase):
    def test_choice_random_position(self):
        test_data: CanGenerateCommandTestData = CanGenerateCommands.generate_test_data()
        position: Position = test_data.bot.choice_random_position(
            test_data.bot.generate_position(type_unit="", troop_size="", i=0, amount=1))
        self.assertEqual(True, self.isInside(test_data.bot.get_location().bounds, position))

    @staticmethod
    def check_unit_id(command: Json, unit_dictionary: UnitDict) -> bool:
        unit_list: UnitList = convert_dictionary_values_to_list(unit_dictionary)
        for unit in unit_list:
            if command["arguments"]["unit_id"] == unit.id:
                return True
        return False

    @staticmethod
    def check_position(command: Json, location: Location) -> bool:
        position: List[float] = command["arguments"]["position"]
        map_bounds: Bounds = location.bounds
        return TestsForCommandGenerationPrivateMethods.isInside(map_bounds, Position(position[0], position[1]))

    @staticmethod
    def isInside(map_bounds: Bounds, position: Position):
        return ((position.x >= map_bounds["SW"].x) and (position.x <= map_bounds["NE"].x)) \
               and ((position.y >= map_bounds["SW"].y) and (position.y <= map_bounds["NE"].y))


if __name__ == '__main__':
    unittest.main()
