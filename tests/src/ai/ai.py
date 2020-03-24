import unittest
from typing import Callable, List

from src.ai.ai import Ai
from src.ai.ai_commands import CommandName
from src.game_data_extractor import UnitDict, UnitList
from src.unit import Unit, UnitType, RegimentType, BaseType, SupportType
from src.unit_state_extractor import unit_states, UnitStatusFromJson


class TestScriptBot(Ai):
    @staticmethod
    def choose_bases(
            choose_function: Callable[[Unit], bool],
            unit_dict: UnitDict) -> UnitList:
        return super().choose_units(choose_function, unit_dict)


class CanChangeUnits(unittest.TestCase):
    @staticmethod
    def change_all_bases(unit: Unit) -> bool:
        return unit.unit_type == BaseType.land_base.__str__()

    @staticmethod
    def generate_empty_unit_dictionary() -> UnitDict:
        return {
            "regiment": [],
            "base": [],
            "support": [],
        }

    @staticmethod
    def generate_test_unit_dictionary() -> UnitDict:
        return {
            "regiment": [Unit().set(0, RegimentType.tank.__str__())],
            "base": [Unit().set(1, BaseType.land_base.__str__())],
            "support": [Unit().set(2, SupportType.truck.__str__())],
        }

    def test_choose_with_correspond_rule(self):
        unit_dictionary: UnitDict = CanChangeUnits.generate_test_unit_dictionary()
        unit_list: UnitList = Ai.choose_units(
            CanChangeUnits.change_all_bases,
            unit_dictionary
        )
        self.assertEqual(unit_list, [unit_dictionary["base"][0]])


class CanChangeCommandForUnit(unittest.TestCase):
    @staticmethod
    def generate_test_unit_dictionary() -> UnitDict:
        return {
            "regiment": [
                Unit().set(UnitStatusFromJson.UNIT_STATUS_STOP, RegimentType.tank.__str__(), unit_states[UnitStatusFromJson.UNIT_STATUS_STOP]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_MARCH, RegimentType.tank.__str__(), unit_states[UnitStatusFromJson.UNIT_STATUS_MARCH]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_ATTACK, RegimentType.tank.__str__(), unit_states[UnitStatusFromJson.UNIT_STATUS_ATTACK]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_DEFENCE, RegimentType.tank.__str__(), unit_states[UnitStatusFromJson.UNIT_STATUS_DEFENCE]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE, RegimentType.tank.__str__(), unit_states[UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE]),
                Unit().set(UnitStatusFromJson.UNIT_STATUS_RETREAT, RegimentType.tank.__str__(), unit_states[UnitStatusFromJson.UNIT_STATUS_RETREAT]),
            ],
            "base": [Unit().set(11, BaseType.land_base.__str__())],
            "support": [Unit().set(12, SupportType.truck.__str__())],
        }

    @staticmethod
    def content_command(command_name: str, where: List[CommandName]) -> bool:
        for value in where:
            if value["commandName"] == command_name:
                return True
        return False

    """
    Таблица состояний
    | stop: true | attack: false | defence: false | UNIT_STATUS_STOP: 1
    | stop: false | attack: false | defence: false | UNIT_STATUS_MARCH: 2
    | stop: true | attack: true | defence: false | UNIT_STATUS_ATTACK: 3
    | stop: true | attack: false | defence: true | UNIT_STATUS_DEFENCE: 4
    | stop: true | attack: true | defence: true | UNIT_STATUS_ATTACK_DEFENCE: 5
    | stop: false | attack: true | defence: false | UNIT_STATUS_RETREAT: 6
    """

    def test_if_stop_then_access_a_move_command(self):
        unit_dictionary: UnitDict = CanChangeCommandForUnit.generate_test_unit_dictionary()

        for attack in [True, False]:
            with self.subTest(attack=attack):
                if attack:
                    for unit_id in [UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE, UnitStatusFromJson.UNIT_STATUS_ATTACK]:
                        with self.subTest(state=unit_id):
                            command_list: List[str] = Ai.generate_access_command_list(
                                unit_dictionary["regiment"][unit_id.value - 1])
                            self.assertEqual(True, CommandName.retreat_or_storm in command_list)
                            self.assertEqual(False, CommandName.move_or_attack in command_list)
                            self.assertEqual(False, CommandName.stop_or_defence in command_list)
                else:
                    for unit_id in [UnitStatusFromJson.UNIT_STATUS_DEFENCE,
                                    UnitStatusFromJson.UNIT_STATUS_STOP]:
                        with self.subTest(state=unit_id):
                            command_list: List[str] = Ai.generate_access_command_list(
                                unit_dictionary["regiment"][unit_id.value - 1])
                            self.assertEqual(True, CommandName.move_or_attack in command_list)
                            self.assertEqual(False, CommandName.retreat_or_storm in command_list)
                            self.assertEqual(False, CommandName.stop_or_defence in command_list)

    def test_if_move_then_access_stop_and_a_move_command(self):
        unit_dictionary: UnitDict = CanChangeCommandForUnit.generate_test_unit_dictionary()

        for attack in [True, False]:
            with self.subTest(attack=attack):
                if attack:
                    command_list: List[str] = Ai.generate_access_command_list(
                        unit_dictionary["regiment"][UnitStatusFromJson.UNIT_STATUS_RETREAT.value - 1])
                    self.assertEqual(True, CommandName.stop_or_defence in command_list)
                    self.assertEqual(True, CommandName.retreat_or_storm in command_list)
                    self.assertEqual(False, CommandName.move_or_attack in command_list)
                else:
                    command_list: List[str] = Ai.generate_access_command_list(
                        unit_dictionary["regiment"][UnitStatusFromJson.UNIT_STATUS_MARCH.value - 1])
                    self.assertEqual(True, CommandName.stop_or_defence in command_list)
                    self.assertEqual(True, CommandName.move_or_attack in command_list)
                    self.assertEqual(False, CommandName.retreat_or_storm in command_list)


class CanGenerateCommandForUnits(unittest.TestCase):
    def test_return_test_commands(self):
        # TODO 7kia потом переделай, протестировано в другом месте
        # see tests/test_route_controller.py
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
