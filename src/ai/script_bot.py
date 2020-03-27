from random import choice as random_choice
from typing import List

from src.ai.ai import Ai
from src.ai.ai_commands import AiCommands, Json
from src.ai.position import Position
from src.game import Game
from src.game_data_extractor import UnitDict
from src.unit import UnitList, Unit


class ScriptBot(Ai):
    # приватные и публичные методы
    # тестируемые методы класса приватные. Как быть?

    # - выбирает случайное подразделение
    # - случайно выбирает одну из доступных, для выбранного подразделения, команду
    # + генерирует команду
    def __init__(self):
        super().__init__()

    def get_commands(self, game: Game) -> List[Json]:
        return [
            AiCommands.generate_move_or_attack_command(1, self.generate_position(None, None, None, None)),
            AiCommands.generate_retreat_or_storm_command(2, self.generate_position(None, None, None, None)),
            AiCommands.generate_stop_or_defence_command(3),
            # AiCommands.generate_take_train_command(4, 5),
            # AiCommands.generate_unload_train_command(4),
        ]

    @staticmethod
    def _get_random_units(unit: Unit) -> bool:
        return random_choice([True, False])

    @staticmethod
    def choose_random_units(unit_dictionary: UnitDict) -> UnitList:
        return Ai.choose_units(
            ScriptBot._get_random_units,
            unit_dictionary
        )

    def _generate_move_or_attack_command(self) -> Json:
        unit_id: int = 0
        position: Position = Position(0, 0)
        return AiCommands.generate_move_or_attack_command(unit_id, position)

    def _generate_retreat_or_storm_command(self) -> Json:
        raise NotImplementedError()

    def _generate_stop_or_defence_command(self) -> Json:
        raise NotImplementedError()

    def _choice_random_position(self) -> List[int]:
        raise NotImplementedError()
