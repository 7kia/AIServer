import unittest
from src.ai.script_bot import ScriptBot


class TestScriptBot(ScriptBot):
    def m(self):
        pass


class TestForScriptBot(unittest.TestCase):
    def test_change_random_amount_units(self):
        self.assertEqual(True, False)

    def test_return_random_command_list_with_random_parameters(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
