from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.game_components.game_state import GameState


class AiAwardsDefiner:
    @classmethod
    def get_awards(cls, current_game_state: GameState,
                   last_game_state: GameState) -> AiAwards:
        awards: AiAwards = AiAwards()

        return awards
