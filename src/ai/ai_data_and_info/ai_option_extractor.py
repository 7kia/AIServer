from src.ai.ai_data_and_info.ai_data import Json
from src.ai.ai_data_and_info.ai_option import AiOption


class AiOptionExtractor:
    @classmethod
    def extract(cls, json: Json) -> AiOption:
        result: AiOption = AiOption()
        result.troopType = json["json"]
        return result
