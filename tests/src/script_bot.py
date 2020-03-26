import unittest
from typing import List

from src.ai.script_bot import ScriptBot
from src.game_data_extractor import UnitList, UnitDict
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
        self.assertEqual(True, False)

    @staticmethod
    def generate_test_script_bot():
        game_id = "3"
        player_id = "31"
        country = "Ukraine"
        input_data: dict = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": "script-bot",
            "ai_name": "intellectual-000",
            "location": CanReturnRandomCommandsWithRandomParameters.generate_mock_location_info(),
            "country": country,
        }
        script_bot: ScriptBot = ScriptBot()
        script_bot.set_location(input_data.location)
        script_bot.set_country(input_data.country)

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


if __name__ == '__main__':
    unittest.main()
