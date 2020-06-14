from typing import List

from src.ai.ai_command_generator import Json
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit import UnitList, Unit
from src.ai.neural_network.neural_network import NeuralNetwork, SHOOTS_TO_SECOND


class ScoutNetwork(NeuralNetwork):
    _TRAIN_TIME: int = 25   # в секундах

    def __init__(self):
        super().__init__()

    def get_commands(self, game_state: GameState) -> List[Json]:
        return super().get_commands(game_state)

    def _generate_commands(self) -> List[Json]:
        return []

    def _generate_access_unit_list(self, game_state: GameState) -> UnitList:
        all_units: UnitList = game_state.game_units.own_units["regiments"]
        result: UnitList = []
        for unit in all_units:
            if (self._troop_type == unit.unit_type) \
                    and self._check_unit_state(unit):
                result.append(unit)
        return result

    def _check_unit_state(self, unit: Unit) -> bool:
        return not unit.state.attack

    def time_end(self) -> bool:
        return self._time_to_tick >= (self._TRAIN_TIME * SHOOTS_TO_SECOND)
