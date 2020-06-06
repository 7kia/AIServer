import json
from typing import List

from src.ai.ai_data_and_info.ai_awards.ai_awards import AiAwards
from src.ai.ai_data_and_info.ai_awards.ai_awards_for_time_dependent_task import AiAwardsForTimeDependentTask
from src.ai.ai_data_and_info.ai_awards.game_time import GameTime
from src.ai.game_components.game_state import GameState


class AiLogger:
    def __init__(self):
        self._end_game_state_file = None
        self._game_state_log_file = None
        self._start_time: GameTime = GameTime()
        self._awards_to_state: List[AiAwards] = []

    def __del__(self):
        self._end_game_state_file.close()
        self._game_state_log_file.close()

    def set_end_game_state_file(self, file):
        self._end_game_state_file = file

    def set_game_state_log_file(self, file):
        self._game_state_log_file = file

    def save_to_game_record_file(self, awards: AiAwards, game_state: GameState):
        if self._not_record_to_files():
            self._set_file_structure()
            self._start_time.set_string_presentation(game_state.current_time)
        self._push_current_state(awards, game_state)

        self._awards_to_state.append(awards)

    def _not_record_to_files(self) -> bool:
        return self._start_time.get_string_presentation() == ""

    def _set_file_structure(self):
        first_string: str = "{\"data\": [\n"
        self._game_state_log_file.write(first_string)
        self._game_state_log_file.seek(len(first_string))

    def _push_current_state(self, awards: AiAwards, game_state: GameState):
        json.dump({
            "game_state": game_state.as_json(),
            "awards": awards.as_json()
        }, self._game_state_log_file, indent=4)
        self._game_state_log_file.write(",\n")

    def get_end_game_state_file_path(self) -> str:
        return self._end_game_state_file.name

    def get_game_log_file_path(self) -> str:
        return self._game_state_log_file.name

    def save_end_game_state(self, awards: AiAwards, game_state: GameState):
        json.dump({
            "game_state": game_state.as_json(),
            "awards": awards.as_json()
        }, self._game_state_log_file, indent=4)
        self._game_state_log_file.write("]}\n")
        self._game_state_log_file.close()

        json.dump({
            "game_state": game_state.as_json(),
            "awards": awards.as_json(),
            "game_duration": self._start_time.get_different_as_string(game_state.current_time),
            "awards_sum": self._generate_awards_sum(awards).as_json(),
        }, self._end_game_state_file, indent=4)
        self._end_game_state_file.close()

    def _generate_awards_sum(self, awards: AiAwards) -> AiAwards:
        self._awards_to_state.append(awards)

        result: AiAwards = awards.clone_empty()
        for awards in self._awards_to_state:
            result += awards
        return result
