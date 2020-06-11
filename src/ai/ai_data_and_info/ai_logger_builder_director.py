from src.ai.ai_data_and_info.ai_info import AiInfo
from src.ai.ai_data_and_info.ai_logger import AiLogger
from src.ai.ai_data_and_info.ai_logger_builder import AiLoggerBuilder
from src.ai.ai_data_and_info.game_info import GameInfo


# TODO 7kia Скорее всего это просто фабрика
class AiLoggerBuilderDirector:
    def __init__(self):
        self._builder = AiLoggerBuilder()

    def create_ai_logger(self, ai_info: AiInfo, game_info: GameInfo):
        try:
            ai_logger: AiLogger = self._builder.create_ai_logger()
            ai_logger.set_end_game_state_file(self._builder.create_end_game_state_file(
                ai_info.ai_address, game_info.ai_options.troop_type
            ))
            ai_logger.set_game_state_log_file(self._builder.create_game_state_log_file(
                ai_info.ai_address, game_info.ai_options.troop_type
            ))
            return ai_logger
        except KeyError as e:
            raise ValueError('Undefined ai type: {}'.format(e.args[0]))
        except Exception as e:
            raise e
