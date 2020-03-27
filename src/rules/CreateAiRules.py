from ..ai.ai_manager import AiManager


class CreateAiRules:
    ai_manager: AiManager = None

    def __init__(self, ai_manager):
        self.ai_manager = ai_manager

    def exist_type(self, ai_type_address):
        return self.ai_manager.exist_type(ai_type_address)

    def exist_name(self, ai_name_address):
        return self.ai_manager.exist_name(ai_name_address)

    def exist_ai(self, game_id, player_id):
        return self.ai_manager.exist_ai(game_id, player_id)



