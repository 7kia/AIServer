import asynctest
import json

from src.location_builder import LocationBuilder
from src.location import Location
from src.routeController import RouteController

AI_SERVER_HOST = 'http://127.0.0.1'
AI_SERVER_PORT = '5000'
AI_SERVER_ADDRESS = AI_SERVER_HOST + ":" + AI_SERVER_PORT


class TestRouteController(asynctest.TestCase):
    @staticmethod
    def generate_create_ai_request(ai_type, ai_name, game_id, player_id):
        return 'http://localhost:5000/ai-server/{0}/{1}/new?gameId={2}&playerId={3}' \
            .format(ai_type, ai_name, game_id, player_id)

    @staticmethod
    def generate_ai_address(game_id, player_id):
        return "/ai-server/{0}/{1}".format(game_id, player_id)

    def test_generate_ai_address(self):
        controller = RouteController()

        game_id = 2
        player_id = 21
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        game_info = [game_id, player_id]
        ai_info = [ai_type, ai_name]

        response = controller.generate_ai_address(game_info, ai_info)
        self.assertEqual(response, (TestRouteController.generate_ai_address(game_id, player_id), 200))

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
    def create_template_controller_with_ai(cls, game_id, player_id, ai_type, ai_name):
        controller = RouteController()
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": ai_type,
            "ai_name": ai_name,
            "location": TestRouteController.generate_mock_location_info(),
            "country": "Ukraine",
        }
        controller.create_ai(input_data)
        return controller

    @classmethod
    def generate_position_to_center_map(cls, ai):
        ai_location = ai.get_location()
        bounds_country = ai_location.bounds_country[ai.get_country()]
        return [
            (bounds_country["NE"].x + bounds_country["SW"].x) / 2,
            (bounds_country["NE"].y + bounds_country["SW"].y) / 2,
        ]

    def test_create_ai(self):
        game_id = "3"
        player_id = "31"
        country = "Ukraine"
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": "script-bot",
            "ai_name": "intellectual-000",
            "location": TestRouteController.generate_mock_location_info(),
            "country": country,
        }

        controller = RouteController()

        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai(game_id, player_id)
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)

        controller.create_ai(input_data)

        # (7kia) For creating connection create ai_socket_connection_info on AI server
        # for understanding that server handle request or no
        try:
            ai = controller.ai_manager.get_ai(game_id, player_id)
            self.assertEqual(ai is not None, True)
            self.assertEqual(
                ai.get_location(),
                LocationBuilder.build(
                    TestRouteController.generate_mock_location_info()
                ))
            self.assertEqual(ai.get_country(), country)

            ai_socket_connection_info = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)
            self.assertEqual(
                ai_socket_connection_info,
                TestRouteController.generate_ai_address(game_id, player_id)
            )
        except Exception as e:
            self.fail(e)

    def test_update_ai(self):
        game_id = "4"
        player_id = "41"
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        controller = TestRouteController.create_template_controller_with_ai(game_id, player_id, ai_type, ai_name)
        json_object = {
            "id": game_id,
            "users": {player_id: {}},
            "loserId": None,
            "status": None,
            "units": {},
            "currentGameTime": None,
            "battleMatrix": None,
        }
        commands: dict = json.loads(controller.update_ai(json_object, [game_id, player_id]))

        position = TestRouteController.generate_position_to_center_map(
            controller.ai_manager.get_ai(game_id, player_id)
        )
        self.assertEqual(
            commands,
            {
                "data":
                    [
                        {
                            "commandName": "move_or_attack",
                            "arguments": {
                                "unit_id": 1,
                                "position": position
                            }
                        },
                        {
                            "commandName": "retreat_or_storm",
                            "arguments": {
                                "unit_id": 2,
                                "position": position
                            }
                        },
                        {
                            "commandName": "stop_or_defence",
                            "arguments": {
                                "unit_id": 3
                            }
                        },
                    ]
            }
        )

    def test_delete_ai(self):
        game_id = "5"
        player_id = "51"
        ai_type = "script-bot"
        ai_name = "intellectual-000"
        controller = TestRouteController.create_template_controller_with_ai(game_id, player_id, ai_type, ai_name)
        message = controller.delete_ai([game_id, player_id])

        self.assertEqual(message, "Ai delete")
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai(game_id, player_id)
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)

    def test_set_ai_unit_positions(self):
        game_id = "6"
        player_id = "61"
        ai_type = "script-bot"
        ai_name = "intellectual-000"
        controller = TestRouteController.create_template_controller_with_ai(game_id, player_id, ai_type, ai_name)

        unit_counts = {
            "tank": {
                "regiment": 1,
            },
            "landbase": {
                "tactic": 1,
            },
        }
        unit_positions = controller.generate_ai_unit_positions(game_id, player_id, unit_counts)

        ai = controller.ai_manager.get_ai(game_id, player_id)
        ai_location: Location = ai.get_location()
        bounds_country = ai_location.bounds_country[ai.get_country()]

        position = [
            (bounds_country["NE"].x + bounds_country["SW"].x) / 2,
            (bounds_country["NE"].y + bounds_country["SW"].y) / 2,
        ]
        expected_country = "Ukraine"
        self.assertEqual(
            json.loads(unit_positions),
            {
                "data":
                [
                    {
                        "commandName": "create_units",
                        "arguments": {
                            "unit_data": [
                                {
                                    "country": expected_country,
                                    "type": "tank",
                                    "position": position,
                                    "troopSize": "regiment",
                                },
                                {
                                    "country": expected_country,
                                    "type": "landbase",
                                    "position": position,
                                    "troopSize": "tactic",
                                }
                            ]
                        }
                    }
                ]
            }
        )


if __name__ == '__main__':
    asynctest.main()
