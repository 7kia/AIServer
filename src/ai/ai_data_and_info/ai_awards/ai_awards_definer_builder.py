from src.ai.ai import Ai
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer import AiAwardsDefiner
from src.ai.ai_data_and_info.ai_awards.ai_awards_definer_for_time_dependent_task import \
    AiAwardsDefinerForTimeDependentTask
from src.ai.ai_data_and_info.ai_awards.awards_definer_params import AwardsDefinerParams


class AiAwardsDefinerBuilder:
    def create(self, ai: Ai) -> AiAwardsDefiner:
        return AiAwardsDefiner(ai.get_awards_definer_params())

    def create_for_time_dependent_task(self, ai: Ai) -> AiAwardsDefinerForTimeDependentTask:
        return AiAwardsDefinerForTimeDependentTask(ai.get_awards_definer_params())

    def set_ai_awards_properties(self, awards_definer: AiAwardsDefiner):
        awards_definer.set_coefficient_composition_generalization(
            self._generate_coefficient_composition_generalization(awards_definer.awards_definer_params)
        )
        awards_definer.set_coefficient_organization_generalization(
            self._generate_coefficient_organization_generalization(awards_definer.awards_definer_params)
        )

    def set_time_dependent_properties(self, awards_definer: AiAwardsDefinerForTimeDependentTask):
        pass

    def _generate_coefficient_composition_generalization(
        self,
        awards_definer_params: AwardsDefinerParams
    ) -> float:
        return awards_definer_params.enemy_unit_composition_amount \
               / awards_definer_params.own_unit_composition_amount

    def _generate_coefficient_organization_generalization(
        self,
        awards_definer_params: AwardsDefinerParams
    ) -> float:
        return awards_definer_params.enemy_unit_organization_amount \
               / awards_definer_params.own_unit_organization_amount
