from tensorflow import Tensor

from src.ai.game_components.command_data_generation import CommandDataGeneration

# TODO 7kia Генерирует только данные нужные для слоя разведки
from src.ai.game_components.game_state import GameState
from src.ai.game_components.unit_observation import UnitObservation
import tensorflow as tf


class TensorGenerator:
    @classmethod
    def generate_for_command_data_generation(cls,
                                             command_data_generation: CommandDataGeneration) -> Tensor:
        return tf.constant(command_data_generation)

    @classmethod
    def generate_for_unit_observation(cls,
                                      unit_observation: UnitObservation) -> Tensor:
        return tf.constant(unit_observation)

    @classmethod
    def generate_for_game_state(cls,
                                current_game_state: GameState) -> Tensor:
        return tf.constant(current_game_state)
