from tensorflow import constant

from src.ai.neural_network.technology_adapter.ai_command import AiCommand


class NetworkAdapter:
    def __init__(self):
        pass

    def train(self,
              command_data_generation: constant,
              unit_observation: constant,
              current_game_state: constant,
              last_game_state: constant) -> AiCommand:
        pass

    def test(self,
             command_data_generation: constant,
             unit_observation: constant,
             current_game_state: constant,) -> AiCommand:
        pass
