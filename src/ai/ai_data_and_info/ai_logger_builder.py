from src.ai.ai_data_and_info.ai_logger import AiLogger


class AiLoggerBuilder:
    def create_ai_logger(self) -> AiLogger:
        return AiLogger()

    def create_end_game_state_file(self, ai_address, troopType):
        pass

    def create_game_state_log_file(self, ai_address, troopType):
        pass
