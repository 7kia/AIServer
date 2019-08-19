from ..ai.aiManager import AiManager


class CreateAiRules:
    ai_manager = None

    def __init__(self, ai_manager):
        self.ai_manager = ai_manager

    def exist_type(self, ai_type):
        return self.ai_manager.exist_type(ai_type)

    def exist_name(self, ai_name):
        return self.ai_manager.exist_name(ai_name)

    def exist_ai(self, game_id, player_id):
        return self.ai_manager.exist_ai(game_id, player_id)



