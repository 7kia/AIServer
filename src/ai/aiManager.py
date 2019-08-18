from flask import jsonify

from .aiBuilder import AiBuilder


class AiManager:
    ai_sockets = {}
    ai_socket_connections = {}
    ai_list = {}
    ai_type_list = {}
    ai_info_list = {}

    def __init__(self, ai_type_list, ai_info_list):
        self.ai_type_list = ai_type_list
        self.ai_info_list = ai_info_list

    @staticmethod
    def init_socket(ai_info, game_info):
        [ai_type, ai_name] = ai_info
        [game_id, player_id] = game_info

        path = "/ai-server/" + ai_name + "/" + ai_type + "/" + str(game_id) + "/" + str(player_id)
        return path

    @classmethod
    def create_ai(cls, game_info, ai_info):
        [game_id, player_id] = game_info
        [ai_type, ai_name] = ai_info

        path = AiManager.init_socket(ai_info, game_info)

        cls.ai_list.update({game_id: {}})
        cls.ai_list[game_id].update({player_id: AiBuilder.create_ai(ai_info, game_info)})

        # TODO create socket

        return path

    @classmethod
    def find_ai(cls, game_id, player_id):
        try:
            return cls.ai_list[str(game_id)][str(player_id)]
        except KeyError as e:
            raise ValueError('Undefined ai type: {0}'.format(e.args[0]))

    @classmethod
    def update_ai(cls, game, game_id, player_id):
        ai = cls.find_ai(game_id, player_id)
        command_list = ai.get_commands(game)
        return jsonify(command_list)

    @classmethod
    def exist_type(cls, ai_type):
        return cls.ai_type_list.get(ai_type) is not None

    @classmethod
    def exist_name(cls, ai_name):
        return cls.ai_info_list.get(ai_name) is not None

    @classmethod
    def exist_ai(cls, game_id, player_id):
        player_list = cls.ai_list.get(game_id)
        if player_list is None:
            return None
        return player_list.get(player_id) is not None
