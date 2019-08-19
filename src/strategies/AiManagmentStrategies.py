from src.ai.aiManager import AiManager


class AiManagmentStrategies:
    def __init__(self, ai_manager):
        self.ai_manager = ai_manager

    def create_ai(self, game_info, ai_info):
        path = self.ai_manager.create_ai(game_info, ai_info)
        return path

    def update_ai(self, game, game_id, player_id):
        return self.ai_manager.update_ai(game, game_id, player_id)

    @staticmethod
    def send_error_message(message):
        return message, 500

    def delete_ai(self, game_id, player_id):
        return self.ai_manager.delete_ai(game_id, player_id)

