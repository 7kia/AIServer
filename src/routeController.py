import json

from src.ai.game_components.game_data_extractor import GameDataExtractor
from .rules.CreateAiRules import CreateAiRules
from .rules.UpdateAiRules import UpdateAiRules
from src.ai.game_components.game_state import GameState
from .ai.ai_manager import AiManager
from typing import List, Dict

from .strategies.AiManagmentStrategies import AiManagmentStrategies

Json = Dict[str, any]


class RouteController:
    def __init__(self):
        self.ai_manager = AiManager()
        self.ai_managment_strategies = AiManagmentStrategies(self.ai_manager)
        self.create_ai_rules = CreateAiRules(self.ai_manager)
        self.update_ai_rules = UpdateAiRules(self.ai_manager)
        self.test_mode: bool = False

    def generate_ai_address(self, game_info, ai_info):
        try:
            [game_id, player_id] = game_info
            [ai_type_address, ai_name_address] = ai_info

            exist_type = self.create_ai_rules.exist_type(ai_type_address)
            exist_name = self.create_ai_rules.exist_name(ai_name_address)
            exist_ai = self.create_ai_rules.exist_ai(game_id, player_id)

            if exist_type is False:
                return AiManagmentStrategies.send_error_message(
                    "Ai type address \'" + ai_type_address + "\' not found"
                ), 500
            if exist_name is False:
                return AiManagmentStrategies.send_error_message(
                    "Ai name address \'" + ai_name_address + "\' not found"
                ), 500
            if exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Game with id=" + game_id + " have player with id=" + player_id
                ), 500

            return self.ai_managment_strategies.generate_ai_address(game_info), 200
        except Exception as e:
            print(e)
            return "", 500

    def update_ai(self, json_object: Dict[str, str], param: List[str]):
        try:
            [game_id, player_id] = param

            game_state: GameState = GameDataExtractor.extract_game(json_object)

            error_message: str = UpdateAiRules.validate_game(game_state, param)
            if error_message != "":
                return AiManagmentStrategies.send_error_message(error_message)

            exist_ai: bool = self.update_ai_rules.exist_ai(game_id, player_id)
            if not exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Ai with player_id={0} not found to game with id={1}".format(game_id, player_id)
                )

            commands = self.ai_managment_strategies.update_ai(game_state, game_id, player_id)
            return RouteController.generate_json_with_double_quotes(commands)
        except Exception as e:
            print(e)
            return str(e)

    def delete_ai(self, param):
        try:
            [game_id, player_id] = param

            exist_ai = self.create_ai_rules.exist_ai(game_id, player_id)
            if not exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Game with id=" + game_id + " have player with id=" + player_id
                )
            return self.ai_managment_strategies.delete_ai(game_id, player_id)
        except Exception as e:
            print(e)
            return e

    @classmethod
    def generate_json_with_double_quotes(cls, commands):
        str_commands = str({"data": commands})
        str_commands = RouteController.replace_one_on_double_quotes(str_commands)
        return str_commands

    @staticmethod
    def replace_one_on_double_quotes(data: str):
        return data.replace("\'", "\"")

    def create_ai(self, data):
        # print("data ={0}".format(data))
        game_id = str(data["game_id"])
        player_id = str(data["player_id"])
        ai_type = data["ai_type"]
        ai_name = data["ai_name"]
        location = data["location"]
        country = data["country"]
        game_state = data["gameState"]
        # print("connect {0} {1}".format(game_id, player_id))
        self.ai_manager.create_ai(
            ai_info=[ai_type, ai_name],
            game_info=[game_id, player_id],
            ai_data=[location, country, game_state],
            test_mode=self.test_mode
        )
        self.ai_manager.add_ai_socket_connection_info(game_id, player_id)

    def generate_ai_unit_positions(self, game_id, player_id, unit_counts):
        ai = self.ai_manager.get_ai(game_id, player_id)
        return RouteController.generate_json_with_double_quotes(
            [ai.generate_unit_positions(unit_counts)]
        )

    @staticmethod
    def generate_ai_list() -> str:
        result = json.load(open("src/ai/AI-list.json"))
        return RouteController.replace_one_on_double_quotes(result.__str__())

    @staticmethod
    def generate_ai_type_list() -> str:
        result = json.load(open("src/ai/AI-type-list.json"))
        return RouteController.replace_one_on_double_quotes(result.__str__())
