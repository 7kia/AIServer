import unittest
from typing import List

from src.ai.game_components.game_data_extractor import Json
from src.ai.game_components.unit_state import UnitState
from src.ai.game_components.unit_state_extractor import UnitStatusFromJson, string_to_int_presentation_unit_state, \
    UnitStateExtractor, int_to_unit_states


class UnitStateExtractorTests(unittest.TestCase):
    @staticmethod
    def generate_test_json() -> List[Json]:
        result: List[Json] = []
        for i in range(1, 7):
            result.append({"_status": str(i)})
        return result

    def test_string_to_int_presentation_unit_state(self):
        test_data: List[Json] = UnitStateExtractorTests.generate_test_json()
        index: int = 0
        int_unit_state_presentation = 1
        for enum_element in UnitStatusFromJson:
            with self.subTest(unit_status=enum_element):
                self.assertEqual(
                    int_unit_state_presentation,
                    string_to_int_presentation_unit_state[test_data[index]["_status"]].value
                )
            index += 1
            int_unit_state_presentation += 1

    def test_extract_state(self):
        test_data: List[Json] = UnitStateExtractorTests.generate_test_json()
        index: int = 0
        int_unit_state_presentation = 1
        for enum_element in UnitStatusFromJson:
            with self.subTest(unit_status=enum_element):
                unit_state: UnitState = UnitStateExtractor.extract_state(test_data[index])
                self.assertEqual(unit_state, int_to_unit_states[enum_element])
                index += 1
                int_unit_state_presentation += 1

if __name__ == '__main__':
    unittest.main()
