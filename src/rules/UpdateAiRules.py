from src.ai.aiManager import AiManager


class UpdateAiRules:
    ai_manager = None

    def __init__(self, ai_manager):
        self.ai_manager = ai_manager

    @classmethod
    def validate_game(cls, game, param):
        [game_id, player_id] = param
        message = ""

        valid_id = game.id == game_id
        if not valid_id:
            message += "Posted game id={0} not equal ai game id ={1};\n".format(game.id, game_id)

        valid_player_id = game.users[str(player_id)] is not None
        if not valid_player_id:
            message += "Posted user id={0} not content to game with id={1};\n".format(game.id, game_id)
        return message

    @classmethod
    def exist_ai(cls, game_id, player_id):
        return cls.ai_manager.exist_ai(game_id, player_id) is not None


