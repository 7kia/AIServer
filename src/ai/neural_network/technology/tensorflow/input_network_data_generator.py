from typing import List, Dict

import numpy as np

from src.ai.game_components.convert_self_to_json import Json
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation


class InputNetworkDataGenerator:
    @classmethod
    def generate_input_data_as_list(cls,
                                    unit_observation: UnitObservation,
                                    current_game_state: GameState) -> List[any]:

        unit_observation_data: Json = unit_observation.as_json()
        person_unit_params_data: Json = current_game_state.person_unit_params.as_json()
        sector_params_data: Json = current_game_state.sector_params.generate_params_for_network()
        input_data: List[any] = []
        for data_set in [unit_observation_data, person_unit_params_data, sector_params_data]:
            for key in data_set.keys():
                add_value: any = data_set[key]
                if isinstance(add_value, (float, int)):
                    input_data.append(data_set[key])
                elif isinstance(add_value, list):
                    input_data.append(cls._handle_list_or_matrix(add_value))
        return input_data

    @classmethod
    def generate_input_data(cls,
                            unit_observation: UnitObservation,
                            current_game_state: GameState) -> Json:

        unit_observation_data: Json = unit_observation.as_json()
        person_unit_params_data: Json = current_game_state.person_unit_params.as_json()
        sector_params_data: Json = current_game_state.sector_params.generate_params_for_network()
        input_data: Json = {}
        for data_set in [unit_observation_data, person_unit_params_data, sector_params_data]:
            for key in data_set.keys():
                add_value: any = data_set[key]
                if isinstance(add_value, (float, int)):
                    input_data[key] = data_set[key]
                elif isinstance(add_value, list):
                    input_data[key] = cls._handle_list_or_matrix(add_value)
        return input_data

    @classmethod
    def _handle_list_or_matrix(cls, add_value: any) -> any:
        if cls.is_position(add_value):
            return np.asarray(add_value)
        elif cls.is_matrix(add_value):
            return np.asarray(cls.do_flat(add_value))

    @staticmethod
    def is_position(value: any) -> bool:
        return len(value) == 2

    @staticmethod
    def is_matrix(value: any) -> bool:
        return len(value) == 4

    @classmethod
    def do_flat(cls, array: List[List[any]]) -> List[any]:
        result: List[any] = [item for sublist in array for item in sublist]
        return result
