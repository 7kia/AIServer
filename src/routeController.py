from flask import jsonify
import json
from .rules.CreateAiRules import CreateAiRules
from .rules.UpdateAiRules import UpdateAiRules
from .strategies.AiManagmentStrategies import AiManagmentStrategies
from .game import Game
from .ai.aiManager import AiManager


class RouteController:
    def __init__(self):
        self.ai_manager = AiManager()
        self.ai_managment_strategies = AiManagmentStrategies(self.ai_manager)
        self.create_ai_rules = CreateAiRules(self.ai_manager)
        self.update_ai_rules = UpdateAiRules(self.ai_manager)

    def generate_ai_address(self, game_info, ai_info):
        try:
            [game_id, player_id] = game_info
            [ai_type, ai_name] = ai_info

            exist_type = self.create_ai_rules.exist_type(ai_type)
            exist_name = self.create_ai_rules.exist_name(ai_name)
            exist_ai = self.create_ai_rules.exist_ai(game_id, player_id)

            if exist_type is False:
                return AiManagmentStrategies.send_error_message(
                    "Ai type \'" + ai_type + "\' not found"
                ), 500
            if exist_name is False:
                return AiManagmentStrategies.send_error_message(
                    "Ai name \'" + ai_name + "\' not found"
                ), 500
            if exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Game with id=" + game_id + " have player with id=" + player_id
                ), 500

            return self.ai_managment_strategies.generate_ai_address(game_info), 200
        except Exception as e:
            print(e)
            return "", 500

    @staticmethod
    def convert_to_game(json_file_content):
        game = Game()
        game.id = json_file_content["id"]
        game.users = json_file_content["users"]
        return game

    def update_ai(self, json_object, param):
        try:
            [game_id, player_id] = param
            game = RouteController.convert_to_game(json_object)

            valid_game = UpdateAiRules.validate_game(game, param)
            exist_ai = self.update_ai_rules.exist_ai(game.id, player_id)

            if valid_game != "":
                return AiManagmentStrategies.send_error_message(valid_game)
            if not exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Ai with player_id={0} not found to game with id={1}".format(game_id, player_id)
                )

            commands = self.ai_managment_strategies.update_ai(game, game_id, player_id)
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
        str_commands = str({"commands": commands})
        str_commands = str_commands.replace("\'", "\"")
        return str_commands

    def create_ai(self, data):
        # print("data ={0}".format(data))
        game_id = str(data["game_id"])
        player_id = str(data["player_id"])
        ai_type = data["ai_type"]
        ai_name = data["ai_name"]
        location = data["location"]
        # print("connect {0} {1}".format(game_id, player_id))

        self.ai_manager.create_ai([ai_type, ai_name], [game_id, player_id], [location])
        self.ai_manager.add_ai_socket_connection_info(game_id, player_id)


