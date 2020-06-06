from src.ai.ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams
from src.ai.game_components.game_data_extractor import Json


class AwardsDefinerParamsExtractor:
    @classmethod
    def extract(cls, data: Json) -> AwardsDefinerParams:
        result: AwardsDefinerParams = AwardsDefinerParams()
        result.own_unit_amount = data["ownUnitAmount"]
        result.enemy_unit_amount = data["enemyUnitAmount"]
        result.own_unit_composition_amount = data["ownUnitCompositionAmount"]
        result.enemy_unit_composition_amount = data["enemyUnitCompositionAmount"]
        result.own_unit_organization_amount = data["ownUnitOrganizationAmount"]
        result.enemy_unit_organization_amount = data["enemyUnitOrganizationAmount"]
        return result
