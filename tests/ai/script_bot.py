import unittest
from typing import List

from src.ai.ai_commands import Json, CommandName
from src.ai.script_bot import ScriptBot
from src.game import Game
from src.game_data_extractor import UnitList, UnitDict, GameDataExtractor
from src.unit import Unit, RegimentType, BaseType, SupportType


class TestScriptBot(ScriptBot):
    def m(self):
        pass


class CanChoiceRandomAmountUnits(unittest.TestCase):
    def test_choice_random_amount_units(self):
        unit_dictionary: UnitDict = CanChoiceRandomAmountUnits.generate_test_unit_dictionary()
        choised_units: UnitList = ScriptBot.choose_random_units(unit_dictionary)

        if len(choised_units) > 0:
            all_units: List[Unit] = CanChoiceRandomAmountUnits.convert_dictionary_values_to_list(unit_dictionary)
            for unit in choised_units:
                self.assertIn(unit, all_units)

    @staticmethod
    def generate_test_unit_dictionary() -> UnitDict:
        return {
            "regiment": [Unit().set(0, RegimentType.tank.__str__())],
            "base": [Unit().set(1, BaseType.land_base.__str__())],
            "support": [Unit().set(2, SupportType.truck.__str__())],
        }

    @staticmethod
    def convert_dictionary_values_to_list(dictionary: dict) -> List[any]:
        result: List[any] = []
        for key, value in dictionary.items():
            result.append(*value)
        return result


class CanReturnRandomCommandsWithRandomParameters(unittest.TestCase):
    def test_return_random_command_list_with_random_parameters(self):
        game_id: int = 3
        player_id: int = 31
        bot_country: str = "Ukraine"
        script_bot: ScriptBot = self.generate_test_script_bot(
            game_id, player_id, bot_country
        )
        game: Game = self.generate_test_game(
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
            "location": CanReturnRandomCommandsWithRandomParameters.generate_mock_location_info(),
            "country": bot_country,
        }
        script_bot: ScriptBot = ScriptBot()
        script_bot.set_location(input_data["location"])
        script_bot.set_country(input_data["country"])
        return script_bot

    @staticmethod
    def generate_mock_location_info():
        return {
            "id": "win_mechanic_test",
            "name": "Win mechanic test",
            "countries": [
                "Novorossia",
                "Ukraine"
            ],
            "bounds": {
                "NE": [
                    50.21621729063866,
                    40.330193359375016
                ],
                "SW": [
                    46.9890206199942,
                    35.3890859375
                ]
            },
            "boundsCountry": {
                "Novorossia": {
                    "NE": [
                        48.12276619505541,
                        39.802849609375016
                    ],
                    "SW": [
                        47.869711326279216,
                        37.74839990234375
                    ]
                },
                "Ukraine": {
                    "NE": [
                        49.767717668674585,
                        37.028801757812516
                    ],
                    "SW": [
                        47.10879329270628,
                        35.32042138671875
                    ]
                }
            },
            "resources": {
                "Novorossia": {
                    "ammo": 100,
                    "fuel": 0,
                    "food": 0,
                    "man": 0
                },
                "Ukraine": {
                    "ammo": 300,
                    "fuel": 0,
                    "food": 0
                }
            },
            "units": {
                "Novorossia": {
                    "tank": {
                        "regiment": 1
                    },
                    "landbase": {
                        "tactic": 1
                    }
                },
                "Ukraine": {
                    "landbase": {
                        "tactic": 1
                    }
                }
            },
            "weapons": {
                "Russia": [
                    1984,
                    1986
                ]
            }
        }

    @staticmethod
    def generate_test_game(game_id: int, player_id: int) -> Game:
        game: Game = Game()
        game.id = game_id
        game.users = {player_id: {}}
        game.unit_dictionary = CanChoiceRandomAmountUnits.generate_test_unit_dictionary()
        # "loserId": None,
        # "status": None,
        # "units": {},
        # "currentGameTime": None,
        # "battleMatrix": None,
        return game

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
