import unittest


class CanGenerateCommands(unittest.TestCase):
    def can_generate_moveOrAttack_command(self):
        self.assertEqual(True, False)

    def can_generate_retreatOrStorm_command(self):
        self.assertEqual(True, False)

    def can_generate_stopOrDefence_command(self):
        self.assertEqual(True, False)


class TestsForCommandGenerationPrivateMethods(unittest.TestCase):
    def choice_random_unit(self):
        self.assertEqual(True, False)

    def choice_random_position(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
