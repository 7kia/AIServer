import asynctest
import requests
import socketio
import json

from src.routeController import RouteController

AI_SERVER_HOST = 'http://127.0.0.1'
AI_SERVER_PORT = '5000'
AI_SERVER_ADDRESS = AI_SERVER_HOST + ":" + AI_SERVER_PORT


class TestRouteController(asynctest.TestCase):
    @staticmethod
    def generate_create_ai_request(ai_type, ai_name, game_id, player_id):
        return 'http://localhost:5000/ai-server/{0}/{1}/new?gameId={2}&playerId={3}'\
            .format(ai_type, ai_name, game_id, player_id)

    @staticmethod
    def generate_ai_address(game_id, player_id):
        return "/ai-server/{0}/{1}/".format(game_id, player_id)

    def test_generate_ai_address(self):
        controller = RouteController()

        game_id = 2
        player_id = 21
        ai_type = "script-bot"
        ai_name = "Intellectual000"

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

    def test_create_ai(self):
        game_id = "3"
        player_id = "31"
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": "script-bot",
            "ai_name": "Intellectual000",
            "location": TestRouteController.generate_mock_location_info()
        }

        controller = RouteController()

        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai(game_id, player_id)
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)

        controller.create_ai(input_data)

        # (7kia) For creating connection create ai_socket_connection_info on AI server
        # for understanding that server handle request or no
        # TODO(7kia) create ai_socket_connection_info on server, here not see it
        try:
            ai = controller.ai_manager.get_ai(game_id, player_id)
            self.assertEqual(ai is not None, True)
            self.assertEqual(ai.location, TestRouteController.generate_mock_location_info())

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
        ai_name = "Intellectual000"

        controller = RouteController()
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": ai_type,
            "ai_name": ai_name,
            "location": TestRouteController.generate_mock_location_info()
        }
        controller.create_ai(input_data)

        json_object = {
            "id": game_id,
            "users": {player_id: {}}
        }
        commands = controller.update_ai(json_object, [game_id, player_id])

        self.assertEqual(
            json.loads(commands),
            {
                "commands":
                [
                    {
                        "arguments": {
                            "arg1": "value1"
                        },
                        "commandName": "moveOrAttack"
                    }
                ]
            }
        )

    def test_delete_ai(self):
        game_id = "5"
        player_id = "51"
        ai_type = "script-bot"
        ai_name = "Intellectual000"

        controller = RouteController()
        input_data = {
            "game_id": game_id,
            "player_id": player_id,
            "ai_type": ai_type,
            "ai_name": ai_name,
            "location": TestRouteController.generate_mock_location_info()
        }
        controller.create_ai(input_data)
        message = controller.delete_ai([game_id, player_id])

        self.assertEqual(message, "Ai delete")
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai(game_id, player_id)
        with self.assertRaises(Exception):
            var = controller.ai_manager.get_ai_socket_connection_info(game_id, player_id)


if __name__ == '__main__':
    asynctest.main()
