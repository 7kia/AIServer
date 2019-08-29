import asynctest
import requests
import socketio
import json

AI_SERVER_HOST = 'http://127.0.0.1'
AI_SERVER_PORT = '5000'
AI_SERVER_ADDRESS = AI_SERVER_HOST + ":" + AI_SERVER_PORT


class TestRestApiServer(asynctest.TestCase):
    @staticmethod
    def generate_create_ai_request(ai_type, ai_name, game_id, player_id):
        return 'http://localhost:5000/ai-server/{0}/{1}/new?gameId={2}&playerId={3}' \
            .format(ai_type, ai_name, game_id, player_id)

    @staticmethod
    def generate_ai_address(game_id, player_id):
        return "/ai-server/{0}/{1}/".format(game_id, player_id)

    def test_generate_ai_address(self):
        game_id = 1
        player_id = 11
        ai_type = "script-bot"
        ai_name = "intellectual-000"

        url = TestRestApiServer.generate_create_ai_request(ai_type, ai_name, game_id, player_id)
        res = requests.get(url)
        response = TestRestApiServer.generate_ai_address(game_id, player_id)
        self.assertEqual(res.text, response)


if __name__ == '__main__':
    asynctest.main()
