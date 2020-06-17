from typing import Dict

from src.ai.game_components.convert_self_to_json import Json


class DatasetData:
    def __init__(self):
        self.input_data: Json = {}
        self.input_data_shapes: Dict[str, tuple] = {}