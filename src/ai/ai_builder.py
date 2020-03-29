from src.ai.ai import Ai
from src.ai.neural_network.neuro_network import NeuroNetwork
from src.ai.script_bot import ScriptBot

AI_TYPES = {
    "test-bot": {"class": Ai},
    "intellectual-000": {"class": ScriptBot},
    "neuron-network": {"class": NeuroNetwork},
}

# TODO 7kia Скорее всего это просто фабрика
class AiBuilder:
    @staticmethod
    def create_ai(ai_info, game_info):
        try:
            [ai_type, ai_name] = ai_info
            [game_id, player_id] = game_info

            new_ai = AI_TYPES[ai_name]["class"]()
            new_ai.id = player_id
            # TODO set AI
            return new_ai
        except KeyError as e:
            raise ValueError('Undefined ai type: {}'.format(e.args[0]))