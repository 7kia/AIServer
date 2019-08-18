from src.ai.aiManager import AiManager


class AiManagmentStrategies:
    ai_manager = None

    def __init__(self, ai_manager):
        self.ai_manager = ai_manager

    @classmethod
    def create_ai(cls, game_info, ai_info):
        path = cls.ai_manager.create_ai(game_info, ai_info)
        return path

    @classmethod
    def update_ai(cls, game, game_id, player_id):
        return cls.ai_manager.update_ai(game, game_id, player_id)

