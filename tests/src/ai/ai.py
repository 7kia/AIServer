import unittest

from src.ai.ai_commands import CommandName


class CanChangeUnits(unittest.TestCase):
    def test_return_list_of_a_unit(self):
        self.assertEqual(True, False)

    def test_throw_exception_if_pass_empty_list(self):
        self.assertEqual(True, False)


class CanChangeCommandForUnit(unittest.TestCase):
    """
    Таблица состояний
    | stop: true | attack: false | defence: false | UNIT_STATUS_STOP: 1
    | stop: false | attack: false | defence: false | UNIT_STATUS_MARCH: 2
    | stop: true | attack: true | defence: false | UNIT_STATUS_ATTACK: 3
    | stop: true | attack: false | defence: true | UNIT_STATUS_DEFENCE: 4
    | stop: true | attack: true | defence: true | UNIT_STATUS_ATTACK_DEFENCE: 5
    | stop: false | attack: true | defence: false | UNIT_STATUS_RETREAT: 6
    """
    def test_if_stop(self):
        for attack in [True, False]:
            with self.subTest(attack=attack):
                if attack:
                    self.assertEqual(False, CommandName.retreat_or_storm)
                else:
                    self.assertEqual(False, CommandName.move_or_attack)

    def test_if_move(self):
        for attack in [True, False]:
            with self.subTest(attack=attack):
                if attack:
                    self.assertEqual(False, CommandName.stop_or_defence)
                    self.assertEqual(False, CommandName.retreat_or_storm)
                else:
                    self.assertEqual(False, CommandName.stop_or_defence)
                    self.assertEqual(False, CommandName.move_or_attack)


if __name__ == '__main__':
    unittest.main()
