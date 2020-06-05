from typing import Dict

from src.ai.ai_data_and_info.ai_option import AiOption

Json = Dict[str, any]


class GameInfo:
    def __init__(self, game_id: int, player_id: int, ai_options: AiOption = None):
        self.game_id: int = game_id
        self.player_id: int = player_id
        self.ai_options: AiOption = ai_options

