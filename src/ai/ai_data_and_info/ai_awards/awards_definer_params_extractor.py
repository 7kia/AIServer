from src.ai.ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams
from src.ai.game_components.game_data_extractor import Json


class AwardsDefinerParamsExtractor:
    @classmethod
    def extract(cls, data: Json) -> AwardsDefinerParams:
        result: AwardsDefinerParams = AwardsDefinerParams()
        result.ownUnitAmount = data["ownUnitAmount"]
        result.enemyUnitAmount = data["enemyUnitAmount"]
        result.ownUnitCompositionAmount = data["ownUnitCompositionAmount"]
        result.enemyUnitCompositionAmount = data["enemyUnitCompositionAmount"]
        return result
