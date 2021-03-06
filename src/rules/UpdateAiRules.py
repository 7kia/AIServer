from typing import List

from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.game_components.game_state import GameState


class UpdateAiRules:
    ai_manager = None

    def __init__(self, ai_manager):
        self.ai_manager = ai_manager

    @staticmethod
    def validate_game(game: GameState, game_info: GameInfo):
        message = ""

        # valid_id = game.id == game_id
        # if not valid_id:
        #     message += "Posted game id={0} not equal ai game id ={1};\n".format(game.id, game_id)

        # TODO 7kia ИИ имеет в users строковый а не числовой id (intelectual-000 вместо 99999)
        # valid_player_id = game.users[str(player_id)] is not None
        # if not valid_player_id:
        #     message += "Posted user id={0} not content to game with id={1};\n".format(player_id, game_id)

        exist_unit_list = game.game_units is not None
        if not exist_unit_list:
            message += "Posted game id={0} not have unit dictionary;\n".format(game_info.game_id)
        return message

    def exist_ai(self, game_id, player_id):
        return self.ai_manager.exist_ai(game_id, player_id)


