from src.ai.ai_data_and_info.ai_data import Json
from src.ai.ai_data_and_info.ai_option import AiOption


class AiOptionExtractor:
    @classmethod
    def extract(cls, json: Json) -> AiOption:
        result: AiOption = AiOption()
        result.troopType = json["troopType"]
        if "isTrain" in json:
            result.is_train = bool(json["isTrain"])
        else:
            result.is_train = False
        return result
