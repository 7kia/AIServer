import unittest


class ForEveryAiUpdate(unittest.TestCase):
    def test_get_commands(self):
        self.assertEqual(True, False)


class InTrainMode(unittest.TestCase):
    def test_get_commands(self):
        self.assertEqual(True, False)

    def test_get_award_and_game_state(self):
        self.assertEqual(True, False)

    def test_in_end_game_get_award_and_game_state(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
