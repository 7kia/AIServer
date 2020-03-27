from typing import List

from src.location import Location


def generate_mock_location_info():
    return Location()


def convert_dictionary_values_to_list(dictionary: dict) -> List[any]:
    result: List[any] = []
    for key, value in dictionary.items():
        result += value
    return result
