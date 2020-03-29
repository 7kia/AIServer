import math
from enum import Enum

from src.ai.game_components.position import Position


class MoveDirection(Enum):
    up: Position = Position(0, 1)
    up_right: Position = Position(math.sqrt(0.5), math.sqrt(0.5))
    right: Position = Position(1, 0)
    down_right: Position = Position(math.sqrt(0.5), -math.sqrt(0.5))
    down: Position = Position(0, -1)
    down_left: Position = Position(-math.sqrt(0.5), -math.sqrt(0.5))
    left: Position = Position(-1, 0)
    up_left: Position = Position(-math.sqrt(0.5), math.sqrt(0.5))
