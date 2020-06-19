from enum import Enum

from src.ai.ai_command_generator import CommandName
from src.ai.game_components.move_direction import MoveDirection


class AiCommand:
    def __init__(self, direction: MoveDirection, distance: float, command_name: str):
        self.direction: MoveDirection = direction
        self.distance: float = distance
        self.command_name: str = command_name
