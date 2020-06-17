from typing import List, Dict

import numpy as np
from tensorflow import TensorSpec

from src.ai.game_components.convert_self_to_json import Json
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation
import tensorflow as tf

from src.ai.neural_network.technology.tensorflow.dataset_data import DatasetData


class InputNetworkDataGenerator:
    def __init__(self):
        self.data = None

    def generate_input_data(self,
                            unit_observation: UnitObservation,
                            current_game_state: GameState) -> Json:#tf.data.Dataset:
        dataset_data: DatasetData = self._generate_dataset_data(
            unit_observation, current_game_state
        )
        output_types = {k: tf.float64 for k in dataset_data.input_data}
        self.data = dataset_data.input_data
        dataset: tf.data.Dataset = tf.data.Dataset.from_generator(
            self._get_input_data_generator,
            output_types=output_types,
            output_shapes=dataset_data.input_data_shapes
        )
        return dataset_data.input_data  # dataset

    def _set_name(self, element_spec):
        result = {}
        for key in element_spec:
            result[key] = TensorSpec(
                shape=element_spec[key].shape,
                dtype=element_spec[key].dtype,
                name=key
            )
        return result

    @classmethod
    def _handle_list_or_matrix(cls, add_value: any, key: str) -> any:
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

    def _get_input_data_generator(self):
        num_samples: int = 1
        for i in range(num_samples):
            batch = {}
            for key, val in self.data.items():
                batch[key] = tf.Variable(val, name=key)
            yield batch

    @classmethod
    def _generate_dataset_data(cls,
                               unit_observation: UnitObservation,
                               current_game_state: GameState) -> DatasetData:
        result: DatasetData = DatasetData()

        unit_observation_data: Json = unit_observation.as_json()
        person_unit_params_data: Json = current_game_state.person_unit_params.as_json()
        sector_params_data: Json = current_game_state.sector_params.generate_params_for_network()
        for data_set in [unit_observation_data, person_unit_params_data, sector_params_data]:
            for key in data_set.keys():
                add_value: any = data_set[key]
                if isinstance(add_value, (float, int)):
                    result.input_data[key] = np.asarray([
                        np.asarray([float(data_set[key])])
                    ])
                    result.input_data_shapes[key] = (1, None)
                elif isinstance(add_value, list):
                    result.input_data[key] =  np.asarray([
                        cls._handle_list_or_matrix(add_value, key)
                    ])
                    result.input_data_shapes[key] = (None, cls._get_size(add_value))
        return result

    @classmethod
    def _get_size(cls,  add_value: any) -> int:
        if cls.is_position(add_value):
            return 2
        elif cls.is_matrix(add_value):
            return 16


