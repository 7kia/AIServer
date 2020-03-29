import unittest

from src.ai.game_components.move_direction import DIRECTIONS
from src.ai.game_components.position import Position
from src.ai.game_components.position_generator import PositionGenerator


class CanGeneratePosition(unittest.TestCase):
    @staticmethod
    def generate_test_map_bounds():
        return {
            "NE": Position(1.0, 1.0),
            "SW": Position(-1.0, -1.0)
        }

    def test_if_position_inside_map_border_return_pass_position(self):
        position: Position = Position(0, 0)
        self.assertEqual(
            position,
            PositionGenerator.move_to_map_border(
                position, self.generate_test_map_bounds()
            )
        )

    def test_if_new_position_out_from_map_border_then_new_position_will_on_near_point_of_map_border(self):
        test_distance: float = 2.0
        for direction in DIRECTIONS:
            with self.subTest(direction=direction):
                input_position: Position = direction.value * test_distance
                result_position: Position = PositionGenerator.move_to_map_border(
                    input_position, self.generate_test_map_bounds()
                )
                expected_position: Position = CanGeneratePosition.generate_expected_position(input_position)
                self.assertEqual(
                    result_position,
                    expected_position
                )

    @staticmethod
    def generate_expected_position(position: Position):
        return Position(
            CanGeneratePosition.generate_expected_coordinate(position.x),
            CanGeneratePosition.generate_expected_coordinate(position.y),
        )

    @staticmethod
    def generate_expected_coordinate(coordinate: float) -> float:
        if coordinate:
            return abs(coordinate) / coordinate
        else:
            return 0


if __name__ == '__main__':
    unittest.main()
