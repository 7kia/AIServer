import unittest
import requests


class TestServer(unittest.TestCase):

    @staticmethod
    def generate_create_ai_request(ai_type, ai_name, game_id, player_id):
        return 'http://localhost:5000/ai-server/{0}/{1}/new?gameId={2}&playerId={3}'\
            .format(ai_type, ai_name, game_id, player_id)

    @staticmethod
    def generate_ai_address(ai_type, game_id, player_id):
        return "/ai-server/Intellectual000/{0}/{1}/{2}".format(ai_type, game_id, player_id)

    def test_create_ai(self):
        game_id = 1
        player_id = 11
        ai_type = "script-bot"
        ai_name = "Intellectual000"

        url = TestServer.generate_create_ai_request(ai_type, ai_name, game_id, player_id)
        res = requests.get(url)
        response = TestServer.generate_ai_address(ai_type, game_id, player_id)
        self.assertEqual(res.text, response)


    @staticmethod
    def generate_update_request(game_id, player_id):
        return 'http://127.0.0.1:5000/ai-server/{0}/{1}/'.format(game_id, player_id)

    def test_update_ai(self):
        game_id = 3
        player_id = 31
        ai_type = "script-bot"
        ai_name = "Intellectual000"

        url = TestServer.generate_create_ai_request(ai_type, ai_name, game_id, player_id)
        create_res = requests.get(url)

        url = TestServer.generate_update_request(game_id, player_id)
        data = ({"id": game_id, "users": {str(player_id): {}}})
        res = requests.post(url, json=data)
        response = """[
  {
    "arguments": {
      "arg1": "value1"
    }, 
    "commandName": "moveOrAttack"
  }
]
"""
        self.assertEqual(res.text, response)


    @staticmethod
    def generate_delete_ai_request(game_id, player_id):
        return 'http://localhost:5000/ai-server/{0}/{1}/delete'.format(game_id, player_id)

    def test_delete_ai(self):
        game_id = 2
        player_id = 2
        ai_type = "script-bot"
        ai_name = "Intellectual000"

        url = TestServer.generate_create_ai_request(ai_type, ai_name, game_id, player_id)
        create_res = requests.get(url)
        url = TestServer.generate_delete_ai_request(game_id, player_id)
        delete_res = requests.get(url)
        self.assertEqual(delete_res.text, "Ai delete")




if __name__ == '__main__':
    unittest.main()
