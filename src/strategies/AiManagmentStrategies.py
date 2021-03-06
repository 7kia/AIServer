from typing import Dict

from src.ai.game_components.game_state import GameState

Json = Dict[str, any]


class AiManagmentStrategies:
    def __init__(self, ai_manager):
        self.ai_manager = ai_manager

    def generate_ai_address(self, game_info):
        return self.ai_manager.generate_ai_adress(game_info)

    def update_ai(self, game_state: GameState, game_id: str, player_id: str):
        return self.ai_manager.update_ai(game_state, game_id, player_id)

    @staticmethod
    def send_error_message(message):
        return message

    def delete_ai(self, game_id, player_id):
        # print("ai_socket_connection_info={0}".format(controller.ai_manager.ai_socket_connection_info))
        self.ai_manager.delete_ai_socket_connection_info(game_id, player_id)
        # print('Close socket {0}'.format(address))
        return self.ai_manager.delete_ai(game_id, player_id)

