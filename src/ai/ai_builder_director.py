from src.ai.ai_builder import AiBuilder
from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.game_info import GameInfo


# TODO 7kia Скорее всего это просто фабрика
class AiBuilderDirector:
    @staticmethod
    def create_ai(ai_info: AiInfo, game_info: GameInfo):
        try:
            return AiBuilder.create_ai(ai_info, game_info)
        except KeyError as e:
            raise ValueError('Undefined ai type: {}'.format(e.args[0]))
        except Exception as e:
            raise e
