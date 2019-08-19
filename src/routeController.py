from flask import jsonify

from .rules.CreateAiRules import CreateAiRules
from .rules.UpdateAiRules import UpdateAiRules
from .strategies.AiManagmentStrategies import AiManagmentStrategies
from .game import Game
from .ai.aiManager import AiManager


class RouteController:
    def __init__(self):
        ai_manager = AiManager()
        self.ai_managment_strategies = AiManagmentStrategies(ai_manager)
        self.create_ai_rules = CreateAiRules(ai_manager)
        self.update_ai_rules = UpdateAiRules(ai_manager)

    def create_ai_for_game(self, request, ai_info):
        try:
            game_id = request.args.get('gameId')
            player_id = request.args.get('playerId')
            game_info = [game_id, player_id]

            [ai_type, ai_name] = ai_info

            exist_type = self.create_ai_rules.exist_type(ai_type)
            exist_name = self.create_ai_rules.exist_name(ai_name)
            exist_ai = self.create_ai_rules.exist_ai(game_id, player_id)

            if exist_type is False:
                return AiManagmentStrategies.send_error_message(
                    "Ai type \'" + ai_type + "\' not found"
                )
            if exist_name is False:
                return AiManagmentStrategies.send_error_message(
                    "Ai name \'" + ai_name + "\' not found"
                )
            if exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Game with id=" + game_id + " have player with id=" + player_id
                )

            return self.ai_managment_strategies.create_ai(game_info, ai_info), 200
        except Exception as e:
            print(e)
            return "", 500

    @staticmethod
    def convert_to_game(json_file_content):
        game = Game()
        game.id = json_file_content["id"]
        game.users = json_file_content["users"]
        return game

    def update_ai(self, request, param):
        try:
            [game_id, player_id] = param
            game = RouteController.convert_to_game(request.get_json())

            valid_game = UpdateAiRules.validate_game(game, param)
            exist_ai = self.update_ai_rules.exist_ai(game.id, player_id)

            if valid_game != "":
                return AiManagmentStrategies.send_error_message(valid_game)
            if not exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Ai with player_id={0} not found to game with id={1}".format(game_id, player_id)
                )
            return jsonify(self.ai_managment_strategies.update_ai(game, game_id, player_id)), 200
        except Exception as e:
            print(e)
            return "", 500

    def delete_ai(self, param):
        try:
            [game_id, player_id] = param

            exist_ai = self.create_ai_rules.exist_ai(game_id, player_id)
            if not exist_ai:
                return AiManagmentStrategies.send_error_message(
                    "Game with id=" + game_id + " have player with id=" + player_id
                )
            return self.ai_managment_strategies.delete_ai(game_id, player_id), 200
        except Exception as e:
            print(e)
            return "", 500

