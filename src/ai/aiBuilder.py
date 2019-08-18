from .aiTypes.neuroNetwork import NeuroNetwork
from .aiTypes.scriptBot import ScriptBot

AI_TYPES = {
    "script-bot": {"class": ScriptBot},
    "neuron-network": {"class": NeuroNetwork},
}


class AiBuilder:
    @staticmethod
    def create_ai(ai_info, game_info):
        try:
            [ai_type, ai_name] = ai_info
            [game_id, player_id] = game_info

            new_ai = AI_TYPES[ai_type]["class"]()
            new_ai.id = player_id
            # TODO set AI
            return new_ai
        except KeyError as e:
            raise ValueError('Undefined ai type: {}'.format(e.args[0]))