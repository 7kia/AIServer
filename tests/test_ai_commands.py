import asynctest

from src.ai.position import Position
from src.location import Bounds
from src.routeController import RouteController
from src.ai.ai_commands import AiCommands


class TestAiCommands(asynctest.TestCase):
    @staticmethod
    def generate_ai_address(game_id, player_id):
        return "/ai-server/{0}/{1}".format(game_id, player_id)

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


    @classmethod
    def create_ai(cls, game_id, player_id, ai_type, ai_name):
        controller = RouteController()
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": ai_type,
            "ai_name": ai_name,
            "location": TestAiCommands.generate_mock_location_info(),
            "country": "Ukraine",
        }
        controller.create_ai(input_data)
        return controller.ai_manager.get_ai(game_id, player_id)

    @classmethod
    def generate_position_to_center_map(cls, ai) -> Position:
        ai_location = ai.get_location()
        bounds_country: Bounds = ai_location.bounds_country[ai.get_country()]
        return Position(
            (bounds_country["NE"].x + bounds_country["SW"].x) / 2,
            (bounds_country["NE"].y + bounds_country["SW"].y) / 2,
        )

    def test_move_or_attack_command(self):
        game_id = "7"
        player_id = "71"
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        ai = TestAiCommands.create_ai(game_id, player_id, ai_type, ai_name)

        position = TestAiCommands.generate_position_to_center_map(ai)
        unit_id = 1
        command = AiCommands.generate_move_or_attack_command(unit_id, position)
        self.assertEqual(
            command,
            {
                "commandName": "move_or_attack",
                "arguments": {
                    "unit_id": unit_id,
                    "position": [position.x, position.y]
                }
            }
        )

    def test_retreat_or_storm_command(self):
        game_id = "8"
        player_id = "81"
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        ai = TestAiCommands.create_ai(game_id, player_id, ai_type, ai_name)

        position = TestAiCommands.generate_position_to_center_map(ai)
        unit_id = 2
        command = AiCommands.generate_retreat_or_storm_command(unit_id, position)
        self.assertEqual(
            command,
            {
                "commandName": "retreat_or_storm",
                "arguments": {
                    "unit_id": unit_id,
                    "position": [position.x, position.y]
                }
            }
        )

    def test_stop_or_defence_command(self):
        game_id = "9"
        player_id = "91"
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        ai = TestAiCommands.create_ai(game_id, player_id, ai_type, ai_name)

        unit_id = 3
        command = AiCommands.generate_stop_or_defence_command(unit_id)
        self.assertEqual(
            command,
            {
                "commandName": "stop_or_defence",
                "arguments": {
                    "unit_id": unit_id
                }
            }
        )

    def test_take_train_command(self):
        game_id = "10"
        player_id = "101"
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        ai = TestAiCommands.create_ai(game_id, player_id, ai_type, ai_name)

        position = TestAiCommands.generate_position_to_center_map(ai)
        unit_id = 4
        passenger_id = 5
        command = AiCommands.generate_take_train_command(unit_id, passenger_id)

        self.assertEqual(
            command,
            {
                "commandName": "take_train",
                "arguments": {
                    "unit_id": unit_id,
                    "passenger_id": passenger_id
                }
            }
        )

    def test_unload_train_command(self):
        game_id = "11"
        player_id = "111"
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        ai = TestAiCommands.create_ai(game_id, player_id, ai_type, ai_name)

        position = TestAiCommands.generate_position_to_center_map(ai)
        unit_id = 5
        command = AiCommands.generate_unload_train_command(unit_id)

        self.assertEqual(
            command,
            {
                "commandName": "unload_train",
                "arguments": {
                    "unit_id": unit_id
                }
            }
        )



if __name__ == '__main__':
    asynctest.main()
