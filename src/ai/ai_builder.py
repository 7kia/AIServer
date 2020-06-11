from src.ai.ai import Ai
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.game_info import GameInfo
from src.ai.neural_network.neural_network import NeuralNetwork
from src.ai.neural_network.scout_network import ScoutNetwork
from src.ai.script_bot import ScriptBot

AI_TYPES = {
    "test-bot": {"class": Ai},
    "intellectual-000": {"class": ScriptBot},
    "neuron-network": {"class": NeuralNetwork},
    "scout-layer": {"class": ScoutNetwork},
}


# TODO 7kia Скорее всего это просто фабрика
class AiBuilder:
    @staticmethod
    def create_ai(ai_info: AiInfo, game_info: GameInfo):
        try:
            new_ai = AI_TYPES[ai_info.ai_address]["class"]()
            new_ai.id = game_info.player_id
            if game_info.ai_options is not None:
                new_ai.set_train_mode(game_info.ai_options.is_train)
                new_ai.set_troop_type(game_info.ai_options.troop_type)
            # TODO set AI
            return new_ai
        except KeyError as e:
            raise ValueError('Undefined ai type: {}'.format(e.args[0]))
