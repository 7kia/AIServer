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
        return path

    @classmethod
    def create_ai_for_game(cls, game_info, ai_info):
        try:
            [game_id, player_id] = game_info

            path = cls.init_socket(ai_info, game_info)

            cls.ai_list.update({game_id: {}})
            cls.ai_list[game_id].update({player_id: AiBuilder.create_ai(ai_info, game_info)})
            return path, 200
        except Exception as e:
            print(e)
            return 500




    @classmethod
    def find_ai(cls, game_id, player_id):
        try:
            return cls.ai_list[str(game_id)][str(player_id)]
        except KeyError as e:
            raise ValueError('Undefined ai type: {0}'.format(e.args[0]))

    @classmethod
    def update_ai(cls, game, param):
        try:
            [game_id, player_id] = param
            ai = cls.find_ai(game_id, player_id)
            command_list = ai.get_commands(game)
            return jsonify(command_list), 200
        except Exception as e:
            print(e)
            return 500








