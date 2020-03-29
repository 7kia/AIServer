from src.ai.game_components.location import Bounds
from src.ai.game_components.position import Position


class PositionGenerator:
    @staticmethod
    def is_inside(map_bounds: Bounds, position: Position) -> bool:
        return (PositionGenerator._in_range(position.x, map_bounds["SW"].x, map_bounds["NE"].x)) \
               and (PositionGenerator._in_range(position.y, map_bounds["SW"].y, map_bounds["NE"].y))

    @staticmethod
    def _in_range(number: float, start: float, end: float) -> bool:
        return (number >= start) and (number <= end)

    @staticmethod
    def move_to_map_border(new_position: Position, map_bounds: Bounds) -> Position:
        result: Position = new_position
        result.x = PositionGenerator._set_border_coordinate(new_position.x, map_bounds["SW"].x, map_bounds["NE"].x)
        result.y = PositionGenerator._set_border_coordinate(new_position.y, map_bounds["SW"].y, map_bounds["NE"].y)
        return result

    @staticmethod
    def _set_border_coordinate(coordinate: float, low_value: float, high_value: float):
        if coordinate < low_value:
            return low_value
        if coordinate > high_value:
            return high_value
        return coordinate
