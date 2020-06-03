import os

from src.ai.ai_data_and_info.ai_logger import AiLogger
import datetime


class AiLoggerBuilder:
    def __init__(self):
        self._divider: str = "__"
        self._directory_divider: str = "/"
        self._end_game_state_directory: str = "end_game_state"
        self._end_game_state_prefix_name: str = "end_game_state"
        self._game_state_log_directory: str = "game_state_log"
        self._game_state_log_prefix_name: str = "game_state_log"

    def create_ai_logger(self) -> AiLogger:
        return AiLogger()

    def create_end_game_state_file(self, ai_address: str, troop_type: str):
        self._create_directory_if_not_created(self._end_game_state_directory)
        return open(
            self._generate_directory_and_file_prefix(
                self._end_game_state_directory, self._end_game_state_prefix_name
            ) + self._generate_time()
            + self._generate_ai_info(ai_address, troop_type)
            + self._generate_suffix_file(), "w+"
        )

    def _create_directory_if_not_created(self, path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        # else:
        #     print("Successfully created the directory %s " % path)

    def _generate_directory_and_file_prefix(self, directory: str, file_prefix: str) -> str:
        return directory + self._directory_divider + file_prefix + self._divider

    def create_game_state_log_file(self, ai_address: str, troop_type: str):
        self._create_directory_if_not_created(self._game_state_log_directory)
        return open(
            self._generate_directory_and_file_prefix(
                self._game_state_log_directory, self._game_state_log_prefix_name
            ) + self._generate_time()
            + self._generate_ai_info(ai_address, troop_type)
            + self._generate_suffix_file(), "w+"
        )

    def _generate_time(self) -> str:
        time = datetime.datetime.now()
        return time.strftime("%b_%d_%Y") + self._divider

    def _generate_ai_info(self, ai_address: str, troop_type: str):
        return ai_address + self._divider + \
               troop_type + self._divider

    @staticmethod
    def _generate_suffix_file() -> str:
        return ".json"
