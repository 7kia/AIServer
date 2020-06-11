from enum import Enum

from src.ai.ai_command_generator import CommandName
from src.ai.game_components.move_direction import MoveDirection


class AiCommand:
    def __init__(self, direction: MoveDirection, command_name: CommandName):
        self.direction: MoveDirection = direction
        self.command_name: CommandName = command_name
