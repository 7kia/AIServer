from typing import List

from src.ai.ai_commands import Json
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation


class NetworkAdapter:
    def __init__(self):
        pass
    
    def train(self, unit_observation: UnitObservation,
              current_game_state: GameState, last_game_state: GameState) -> List[Json]:
        pass

    def test(self, unit_observation: UnitObservation,
             current_game_state: GameState) -> List[Json]:
        pass
