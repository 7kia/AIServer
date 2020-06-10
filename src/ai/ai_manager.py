import json

from .ai import Ai
from .ai_builder_director import AiBuilderDirector
from src.ai.game_components.location_builder import LocationBuilder
from src.ai.game_components.game_state import GameState
from src.ai.ai_data_and_info.ai_data import AiData
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from .ai_data_and_info.ai_awards.ai_awards_definer_director import AiAwardsDefinerDirector
from .ai_data_and_info.ai_logger import AiLogger
from .ai_data_and_info.ai_logger_builder_director import AiLoggerBuilderDirector
from src.ai.ai_data_and_info.ai_awards.awards_definer_params_extractor import AwardsDefinerParamsExtractor
from .neural_network.technology_adapter.network_technology_adapter_director import NetworkTechnologyAdapterDirector


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
        self.ai_logger_director = AiLoggerBuilderDirector()
        self._ai_logger_list = {}
        self._ai_awards_definer_director = AiAwardsDefinerDirector()
        self._ai_awards_definer_list = {}
        self._network_technology_adapter_director = NetworkTechnologyAdapterDirector()

    def get_ai(self, game_id, player_id):
        return self._ai_list[game_id][player_id]

    def get_ai_socket_connection_info(self, game_id, player_id):
        return self._ai_socket_connection_info[game_id][player_id]

    @staticmethod
    def generate_ai_address(game_id, player_id):
        return "/ai-server/{0}/{1}".format(game_id, player_id)

    def create_ai(self, ai_info: AiInfo, game_info: GameInfo, ai_data: AiData,
                  test_mode: bool = False):
        if not test_mode and (ai_info.ai_address == "test-bot"):
            raise BaseException("In production mode try create test-bot")

        game_id = game_info.game_id
        player_id = game_info.player_id
        self._add_ai_to_list(game_id, player_id, ai_info, game_info)
        self._set_new_ai(ai_info, game_info, ai_data)

    def _add_ai_to_list(self, game_id: int, player_id: int,
                        ai_info: AiInfo, game_info: GameInfo):
        self._ai_list.update({game_id: {}})
        self._ai_list[game_id].update({
            player_id: AiBuilderDirector.create_ai(ai_info, game_info)
        })

    def _set_new_ai(self, ai_info: AiInfo, game_info: GameInfo,
                    ai_data: AiData):
        ai: Ai = self._ai_list[game_info.game_id][game_info.player_id]
        ai.set_location(LocationBuilder.build(ai_data.location))
        ai.set_country(ai_data.country)
        ai.set_graph_density(ai_data.game_state["graphDensity"])
        ai.set_awards_definer_params(AwardsDefinerParamsExtractor.extract(ai_data.game_state))
        self._add_ai_awards_definer_to_list(ai, game_info)

        ai.set_network_adapter(self._network_technology_adapter_director
                                .generate_scout_network_adapter(ai_info))
        if ai.is_train():
            self._add_ai_logger_to_list(ai_info, game_info)

    def _add_ai_awards_definer_to_list(self, ai: Ai, game_info: GameInfo):
        self._ai_awards_definer_list.update({game_info.game_id: {}})
        self._ai_awards_definer_list[game_info.game_id].update({
            game_info.player_id: self._ai_awards_definer_director.create_for_ai(ai)
        })

    def _add_ai_logger_to_list(self, ai_info: AiInfo, game_info: GameInfo):
        self._ai_logger_list.update({game_info.game_id: {}})
        self._ai_logger_list[game_info.game_id].update({
            game_info.player_id: self.ai_logger_director.create_ai_logger(ai_info, game_info)
        })

    def add_ai_socket_connection_info(self, game_id, player_id):
        self._ai_socket_connection_info.update({game_id: {}})
        self._ai_socket_connection_info[game_id].update({player_id: AiManager.generate_ai_address(game_id, player_id)})

    def delete_ai_socket_connection_info(self, game_id, player_id):
        del self._ai_socket_connection_info[str(game_id)][str(player_id)]
        if self._ai_socket_connection_info[str(game_id)] == {}:
            del self._ai_socket_connection_info[str(game_id)]

    def generate_ai_adress(self, game_info: GameInfo):
        return AiManager.generate_ai_address(game_info.game_id, game_info.player_id)

    def update_ai(self, game_state: GameState, game_id: str, player_id: str):
        ai: Ai = self.__find_ai(game_id, player_id)
        command_list = ai.get_commands(game_state)
        if ai.is_train():
            ai_logger: AiLogger = self.__find_ai_logger(game_id, player_id)
            ai_awards_definer: AiAwardsDefiner = self.__find_ai_awards_definer(game_id, player_id)
            ai_awards: AiAwards = ai_awards_definer.get_awards(
                ai.get_current_game_state(),
                ai.get_last_game_state()
            )
            ai_logger.save_to_game_record_file(ai_awards, game_state)
        return command_list

    def __find_ai(self, game_id: str, player_id: str) -> Ai:
        try:
            return self._ai_list[str(game_id)][str(player_id)]
        except KeyError as e:
            raise ValueError('Ai with key \"{0}\" not found'.format(e.args[0]))

    def __find_ai_logger(self, game_id: str, player_id: str) -> AiLogger:
        try:
            return self._ai_logger_list[str(game_id)][str(player_id)]
        except KeyError as e:
            raise ValueError('Ai_logger with key \"{0}\" not found'.format(e.args[0]))

    def __find_ai_awards_definer(self, game_id: str, player_id: str) -> AiAwardsDefiner:
        try:
            return self._ai_awards_definer_list[str(game_id)][str(player_id)]
        except KeyError as e:
            raise ValueError('AiAwardsDefiner with key \"{0}\" not found'.format(e.args[0]))

    def delete_ai(self, game_id, player_id):
        ai: Ai = self.__find_ai(game_id, player_id)
        if ai.is_train():
            self._save_end_game_state(game_id, player_id)
            del self._ai_logger_list[str(game_id)][str(player_id)]
            if self._ai_logger_list[str(game_id)] == {}:
                del self._ai_logger_list[str(game_id)]

        del self._ai_list[str(game_id)][str(player_id)]
        if self._ai_list[str(game_id)] == {}:
            del self._ai_list[str(game_id)]
        return AiManager.get_succsess_delete_message()

    def _save_end_game_state(self, game_id, player_id):
        ai: Ai = self.__find_ai(game_id, player_id)
        ai_awards_definer: AiAwardsDefiner = self.__find_ai_awards_definer(game_id, player_id)
        ai_awards: AiAwards = ai_awards_definer.get_awards(
            ai.get_current_game_state(),
            ai.get_last_game_state()
        )
        ai_logger: AiLogger = self.__find_ai_logger(game_id, player_id)
        ai_logger.save_end_game_state(ai_awards, ai.get_current_game_state())

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
