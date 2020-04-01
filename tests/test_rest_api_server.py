import asynctest
import requests
import socketio
import json

from src.routeController import Json

AI_SERVER_HOST = 'http://127.0.0.1'
AI_SERVER_PORT = '5000'
AI_SERVER_ADDRESS = AI_SERVER_HOST + ":" + AI_SERVER_PORT


class TestRestApiServer(asynctest.TestCase):
    @staticmethod
    def generate_create_ai_request(ai_type, ai_name, game_id, player_id):
        return f'{TestRestApiServer.generate_server_address()}' \
               f'/ai-server/{ai_type}/{ai_name}/new?gameId={game_id}&playerId={player_id}'

    @staticmethod
    def generate_server_address() -> str:
        return "http://localhost:5000"

    @staticmethod
    def generate_ai_address(game_id, player_id):
        return f"/ai-server/{game_id}/{player_id}"

    def test_generate_ai_address(self):
        game_id = 1
        player_id = 11
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        url = TestRestApiServer.generate_create_ai_request(ai_type, ai_name, game_id, player_id)
        res = requests.get(url)
        response = TestRestApiServer.generate_ai_address(game_id, player_id)
        self.assertEqual(res.text, response)

    def test_get_ai_list(self):
        res = requests.get(self.generate_get_ai_list_request())
        response: Json = json.loads(res.text)
        self.assertEqual(
            True,
            "Intellectual000" in response.keys()
        )

    @staticmethod
    def generate_get_ai_list_request() -> str:
        return TestRestApiServer.generate_server_address() + "/get-ai-list"

    def test_get_ai_type_list(self):
        res = requests.get(self.generate_get_ai_type_list_request())
        self.assertEqual(
            True,
            "script-bot" in json.loads(res.text).keys()
        )
        self.assertEqual(
            True,
            "neuron-network" in json.loads(res.text).keys()
        )

    @staticmethod
    def generate_get_ai_type_list_request() -> str:
        return TestRestApiServer.generate_server_address() + "/get-ai-type-list"


if __name__ == '__main__':
    asynctest.main()
