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

    def create_ai(self, game_info, ai_info):
        [game_id, player_id] = game_info
        [ai_type, ai_name] = ai_info

        path = AiManager.init_socket(ai_info, game_info)

        self.ai_list.update({game_id: {}})
        self.ai_list[game_id].update({player_id: AiBuilder.create_ai(ai_info, game_info)})

        # TODO create socket

        return path

    def find_ai(self, game_id, player_id):
        try:
            return self.ai_list[str(game_id)][str(player_id)]
        except KeyError as e:
            raise ValueError('Undefined ai type: {0}'.format(e.args[0]))

    def update_ai(self, game, game_id, player_id):
        ai = self.find_ai(game_id, player_id)
        command_list = ai.get_commands(game)
        return jsonify(command_list)

    def delete_ai(self, game_id, player_id):
        del self.ai_list[str(game_id)][str(player_id)]
        if self.ai_list[str(game_id)] == {}:
            del self.ai_list[str(game_id)]
        return "Ai delete"

    def exist_type(self, ai_type):
        type = self.ai_type_list.get(ai_type)
        return type is not None

    def exist_name(self, ai_name):
        name = self.ai_info_list.get(ai_name)
        return name is not None

    def exist_ai(self, game_id, player_id):
        player_list = self.ai_list.get(str(game_id))
        if player_list is None:
            return None
        return player_list.get(str(player_id)) is not None
