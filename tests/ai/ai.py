import unittest
from typing import List

from src.ai.ai import Ai
from src.ai.ai_commands import CommandName
from src.fortest.test_data_generator import TestDataGenerator
from src.ai.game_components.game_data_extractor import UnitDict, UnitList
from src.ai.game_components.unit import Unit, RegimentType, BaseType, SupportType
from src.ai.game_components.unit_state_extractor import UnitStatusFromJson


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
    def check_access_commands(where: List[str], expected: List[str]):
        for command_name in where:
            if command_name not in expected:
                raise AssertionError("Command {0} must be not there".format(command_name))

    @staticmethod
    def generate_and_check_access_commands(
            unit_dictionary: UnitDict, unit_id: int,
            access_commands: List[str]):
        command_list: List[str] = Ai.generate_access_command_list(
            unit_dictionary["regiment"][unit_id.value - 1]
        )
        CanChangeCommandForUnit.check_access_commands(command_list, access_commands)

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
        unit_dictionary: UnitDict = TestDataGenerator.generate_unit_with_various_state()

        for attack in [True, False]:
            with self.subTest(attack=attack):
                if attack:
                    for unit_id in [UnitStatusFromJson.UNIT_STATUS_ATTACK_DEFENCE,
                                    UnitStatusFromJson.UNIT_STATUS_ATTACK]:
                        with self.subTest(state=unit_id):
                            CanChangeCommandForUnit.generate_and_check_access_commands(
                                unit_dictionary, unit_id, [CommandName.retreat_or_storm]
                            )
                else:
                    for unit_id in [UnitStatusFromJson.UNIT_STATUS_DEFENCE,
                                    UnitStatusFromJson.UNIT_STATUS_STOP]:
                        with self.subTest(state=unit_id):
                            CanChangeCommandForUnit.generate_and_check_access_commands(
                                unit_dictionary, unit_id, [CommandName.move_or_attack]
                            )

    def test_if_move_then_access_stop_and_a_move_command(self):
        unit_dictionary: UnitDict = TestDataGenerator.generate_unit_with_various_state()

        for attack in [True, False]:
            with self.subTest(attack=attack):
                if attack:
                    for unit_id in [UnitStatusFromJson.UNIT_STATUS_RETREAT]:
                        CanChangeCommandForUnit.generate_and_check_access_commands(
                            unit_dictionary, unit_id,
                            [CommandName.stop_or_defence, CommandName.retreat_or_storm]
                        )
                else:
                    for unit_id in [UnitStatusFromJson.UNIT_STATUS_MARCH]:
                        CanChangeCommandForUnit.generate_and_check_access_commands(
                            unit_dictionary, unit_id,
                            [CommandName.stop_or_defence, CommandName.move_or_attack]
                        )


class CanGenerateCommandForUnits(unittest.TestCase):
    def test_return_test_commands(self):
        # TODO 7kia потом переделай, протестировано в другом месте
        # see tests/test_route_controller.py
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
