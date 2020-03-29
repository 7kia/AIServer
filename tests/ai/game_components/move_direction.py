import math
import unittest

from src.ai.game_components.move_direction import MoveDirection


class MoveDirectionTests(unittest.TestCase):
    def test_equal_to_a_unit_vector(self):
        for direction in MoveDirection:
            with self.subTest(direction=direction):
                self.assertEqual(
                    True,
                    math.isclose(
                        1, (direction.value.x**2 + direction.value.y**2)
                        , rel_tol=1e-5
                    )
                )



if __name__ == '__main__':
    unittest.main()
