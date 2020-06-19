import math
from enum import Enum
from typing import List

from src.ai.game_components.position import Position


# 7kia В качестве вектора был выбран единичный вектор
class MoveDirection(Enum):
    up: Position = Position(0, 1)
    up_right: Position = Position(math.sqrt(0.5), math.sqrt(0.5))
    right: Position = Position(1, 0)
    down_right: Position = Position(math.sqrt(0.5), -math.sqrt(0.5))
    down: Position = Position(0, -1)
    down_left: Position = Position(-math.sqrt(0.5), -math.sqrt(0.5))
    left: Position = Position(-1, 0)
    up_left: Position = Position(-math.sqrt(0.5), math.sqrt(0.5))


DIRECTIONS: List[MoveDirection] = []
for direction in MoveDirection:
    DIRECTIONS.append(direction)

DISTANCE_COEFFICIENT: float = 100  # Задаётся на ИИ-сервере


class LengthDistance(Enum):
    short_distance: float = 0.5 / DISTANCE_COEFFICIENT  # km 5
    long_distance: float = 1 / DISTANCE_COEFFICIENT  # km 10


class LengthDistanceIndex(Enum):
    short_distance: int = 0
    long_distance: int = 1  # km 10


length_distance_variant_amount: int = 0
length_variant: List[float] = []
for variant in LengthDistance:
    length_variant.append(variant.value)
    length_distance_variant_amount += 1
