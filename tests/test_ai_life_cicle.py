import unittest
import requests

from src.ai.aiManager import AiManager
from src.game import Game


class AiLifeCircle(unittest.TestCase):

    @staticmethod
    def generate_ai_address(ai_type, game_id, player_id):
        return "/ai-server/Intellectual000/{0}/{1}/{2}".format(ai_type, game_id, player_id)

    def test_ai_create(self):
        self.ai_manager = AiManager()

        game_id = "4"
        player_id = "41"
        ai_type = "script-bot"
        ai_name = "Intellectual000"

        with self.assertRaises(Exception):
            var = self.ai_manager.ai_list[game_id][player_id]
        with self.assertRaises(Exception):
            var = self.ai_manager.ai_sockets[game_id][player_id]
        with self.assertRaises(Exception):
            var = self.ai_manager.ai_socket_connections[game_id][player_id]

        path = self.ai_manager.create_ai([game_id, player_id], [ai_type, ai_name])
        self.assertEqual(path, AiLifeCircle.generate_ai_address(ai_type, game_id, player_id))

        try:
            ai = self.ai_manager.ai_list[game_id][player_id]
            ai_socket = self.ai_manager.ai_sockets[game_id][player_id]
            ai_socket_connection = self.ai_manager.ai_socket_connections[game_id][player_id]
            self.assertEqual(ai is not None, True)
            self.assertEqual(ai_socket is not None, True)
            self.assertEqual(ai_socket_connection is not None, True)
        except Exception as e:
            self.fail("socket not created")

    def test_ai_update(self):
        self.ai_manager = AiManager()
        game_id = "5"
        player_id = "51"
        ai_type = "script-bot"
        ai_name = "Intellectual000"

        path = self.ai_manager.create_ai([game_id, player_id], [ai_type, ai_name])

        game = Game()
        game.id = game_id
        game.users = {"users": {str(player_id): {}}}

        commands = self.ai_manager.update_ai(game, game_id, player_id)
        self.assertEqual(commands, [
          {
            "arguments": {
              "arg1": "value1"
            },
            "commandName": "moveOrAttack"
          }
        ])

    def test_ai_delete(self):
        self.ai_manager = AiManager()
        game_id = "6"
        player_id = "61"
        ai_type = "script-bot"
        ai_name = "Intellectual000"

        path = self.ai_manager.create_ai([game_id, player_id], [ai_type, ai_name])

        message = self.ai_manager.delete_ai(game_id, player_id)
        self.assertEqual("Ai delete", message)
        with self.assertRaises(Exception):
            self.ai_manager.ai_list[game_id][player_id]
        with self.assertRaises(Exception):
            self.ai_manager.ai_sockets[game_id][player_id]
        with self.assertRaises(Exception):
            self.ai_manager.ai_socket_connections[game_id][player_id]


    # def test_ai_life_circle(self):
    #     game_id = 4
    #     player_id = 41
    #     ai_type = "script-bot"
    #     ai_name = "Intellectual000"
    #
    #     # self.ai_manager.c

if __name__ == '__main__':
    unittest.main()



