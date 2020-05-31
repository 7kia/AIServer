import json
from typing import List

from .ai_builder_director import AiBuilderDirector
from src.ai.game_components.location_builder import LocationBuilder
from src.ai.game_components.game_state import GameState


class AiManager:
    def __init__(self):
        ai_type_list_file = open("src/ai/AI-type-list.json")
        ai_info_list_file = open("src/ai/AI-list.json")
        ai_type_list = json.load(ai_type_list_file)
        ai_info_list = json.load(ai_info_list_file)
        ai_type_list_file.close()
        ai_info_list_file.close()

        self.ai_type_list = ai_type_list
        self.ai_info_list = ai_info_list
        self._ai_list = {}
        self._ai_socket_connection_info = {}

    def get_ai(self, game_id, player_id):
        return self._ai_list[game_id][player_id]

    def get_ai_socket_connection_info(self, game_id, player_id):
        return self._ai_socket_connection_info[game_id][player_id]

    @staticmethod
    def generate_ai_address(game_id, player_id):
        return "/ai-server/{0}/{1}".format(game_id, player_id)

    def create_ai(self, ai_info: List[str], game_info: List[any], ai_data: List[any],
                  test_mode: bool = False):
        [game_id, player_id, ai_options] = game_info

        [ai_type, ai_address] = ai_info
        if not test_mode and (ai_address == "test-bot"):
            raise BaseException("In production mode try create test-bot")

        self._ai_list.update({game_id: {}})
        self._ai_list[game_id].update({player_id: AiBuilderDirector.create_ai(ai_info, game_info)})

        [location, country, game_state] = ai_data
        self._ai_list[game_id][player_id].set_location(LocationBuilder.build(location))
        self._ai_list[game_id][player_id].set_country(country)
        self._ai_list[game_id][player_id].set_graph_density(game_state["graphDensity"])

    def add_ai_socket_connection_info(self, game_id, player_id):
        self._ai_socket_connection_info.update({game_id: {}})
        self._ai_socket_connection_info[game_id].update({player_id: AiManager.generate_ai_address(game_id, player_id)})

    def delete_ai_socket_connection_info(self, game_id, player_id):
        del self._ai_socket_connection_info[str(game_id)][str(player_id)]
        if self._ai_socket_connection_info[str(game_id)] == {}:
            del self._ai_socket_connection_info[str(game_id)]

    def generate_ai_adress(self, game_info):
        [game_id, player_id] = game_info
        return AiManager.generate_ai_address(game_id, player_id)

    def __find_ai(self, game_id: str, player_id: str):
        try:
            return self._ai_list[str(game_id)][str(player_id)]
        except KeyError as e:
            raise ValueError('Undefined ai type: {0}'.format(e.args[0]))

    def update_ai(self, game_state: GameState, game_id: str, player_id: str):
        ai = self.__find_ai(game_id, player_id)
        command_list = ai.get_commands(game_state)
        return command_list

    def delete_ai(self, game_id, player_id):
        del self._ai_list[str(game_id)][str(player_id)]
        if self._ai_list[str(game_id)] == {}:
            del self._ai_list[str(game_id)]
        return AiManager.get_succsess_delete_message()

    def exist_type(self, ai_type_address):
        for key in self.ai_type_list:
            if self.ai_type_list[key]["address"] == ai_type_address:
                return True
        return False

    def exist_name(self, ai_name_address):
        for key in self.ai_info_list:
            if self.ai_info_list[key]["address"] == ai_name_address:
                return True
        return False

    def exist_ai(self, game_id, player_id):
        player_list = self._ai_list.get(str(game_id))
        if player_list is None:
            return None
        return player_list.get(str(player_id)) is not None

    @classmethod
    def get_succsess_delete_message(cls):
        return "Ai delete"
