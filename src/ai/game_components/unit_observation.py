from src.ai.game_components.convert_self_to_json import ConvertSelfToJson, Json
from src.ai.game_components.position import Position
from src.ai.game_components.position_int import PositionInt
from src.ai.game_components.sector_params import SectorParams
from src.ai.game_components.unit import Unit


class UnitObservation(ConvertSelfToJson):
    def __init__(self):
        self.own_organization: float = 0
        self.own_composition: float = 0
        self.sector: PositionInt = PositionInt()

        self.own_sum_info: float = 0
        self.own_max_info: float = 0
        self.enemy_sum_info: float = 0
        self.enemy_max_info: float = 0

    def set(self, sector_params: SectorParams, unit: Unit):
        self.own_organization = unit.organization
        self.own_composition = unit.composition

        self.sector = sector_params.find_unit_index(unit)
        self.own_sum_info = sector_params.own_sum_info[self.sector.y][self.sector.x]
        self.own_max_info = sector_params.own_max_info[self.sector.y][self.sector.x]
        self.enemy_sum_info = sector_params.enemy_sum_info[self.sector.y][self.sector.x]
        self.enemy_max_info = sector_params.enemy_max_info[self.sector.y][self.sector.x]

    def as_json(self) -> Json:
        return {
            self._generate_prefix() + "own_organization": self.own_organization,
            self._generate_prefix() + "own_composition": self.own_composition,
            self._generate_prefix() + "sector": self.sector.as_array(),
            self._generate_prefix() + "own_sum_info": self.own_sum_info,
            self._generate_prefix() + "own_max_info": self.own_max_info,
            self._generate_prefix() + "enemy_sum_info": self.enemy_sum_info,
            self._generate_prefix() + "enemy_max_info": self.enemy_max_info,
        }

    def _generate_prefix(self) -> str:
        return "unit_observation__"

