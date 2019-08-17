import random

from flask import abort, jsonify
import socket
from .aiBuilder import AiBuilder


class Controller:
    ai_sockets = {}
    ai_socket_connections = {}
    ai_list = {}

    def __init__(self):
        pass

    @classmethod
    def init_socket(cls, ai_info, game_info):
        [ai_type, ai_name] = ai_info
        [game_id, player_id] = game_info

        path = "/ai-server/" + ai_name + "/" + ai_type + "/" + str(game_id) + "/" + str(player_id)
        cls.ai_sockets.update({game_id: {player_id: socket.socket()}})
        current_socket = cls.ai_sockets[game_id][player_id]
        current_socket.bind(("", 5001))
        current_socket.listen(1)

    @classmethod
    def create_ai_for_game(cls, game_info, ai_info):
        [game_id, player_id] = game_info

        cls.init_socket(ai_info, game_info)
        current_socket = cls.ai_sockets[game_id][player_id]

        conn, addr = current_socket.accept()
        cls.ai_socket_connections[game_id][player_id] = conn

        cls.ai_list[game_id][player_id] = AiBuilder.create_ai(ai_info, game_info)

        return addr, 200

    @classmethod
    def find_ai(cls, game_id, player_id):
        try:
            return cls.ai_list[game_id][player_id]
        except KeyError as e:
            raise ValueError('Undefined ai type: {}'.format(e.args[0]))
        return None

    @classmethod
    def update_ai(cls, game, param):
        [game_id, player_id] = param
        ai = cls.find_ai(game_id, player_id)
        commandList = ai.get_commands(game)
        return jsonify(commandList)






